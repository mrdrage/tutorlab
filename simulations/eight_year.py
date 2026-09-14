from __future__ import annotations

import random
from typing import Any

from engine.adaptive_engine import decide
from engine.objective_stack import complete_current, current_objective, push_recovery, recovery_depth, start_objective
from engine.reliability_state import calibrated_state
from simulations.eight_year_profiles import PROFILES_8Y, EightYearProfile


def _clamp(value: float) -> float:
    return max(0.0, min(1.0, value))


def _support(action: str, dependence: float, item: int) -> str:
    if action == "reassess":
        return "none"
    if dependence >= 0.7:
        return ("worked_support", "structured_prompt", "structured_prompt", "light_prompt", "none", "none")[item % 6]
    if action == "recover":
        return ("worked_support", "structured_prompt", "light_prompt", "none", "none", "none")[item % 6]
    return ("structured_prompt", "light_prompt", "none", "none", "none", "none")[item % 6]


def _event(
    profile: EightYearProfile,
    competency_id: str,
    latent_skill: float,
    *,
    stage_index: int,
    session_index: int,
    item_index: int,
    action: str,
    rng: random.Random,
    missing_prerequisite: str | None,
) -> dict[str, Any]:
    dependence = profile.support_dependence if recovery_depth_hint(competency_id, profile) == 0 else max(0.0, profile.support_dependence - 0.2)
    support = _support(action, dependence, item_index)
    support_boost = {"none": 0.0, "light_prompt": 0.05, "structured_prompt": 0.13, "worked_support": 0.21}[support]
    independence_penalty = dependence * (0.24 if support == "none" else 0.08)
    probability = _clamp(latent_skill + support_boost - independence_penalty + rng.gauss(0.0, profile.volatility))
    draw = rng.random()
    if draw < probability - 0.08:
        status = "correct"
    elif draw < probability + 0.08:
        status = "partially_correct"
    else:
        status = "incorrect"

    outcome: dict[str, Any] = {"status": status}
    context = "routine"
    if item_index in {4, 5}:
        context = "near_transfer"
        transfer = latent_skill + profile.transfer_offset - independence_penalty + rng.gauss(0.0, profile.volatility)
        outcome["transfer_success"] = _clamp(transfer)
    if item_index == 3:
        outcome["explanation_quality"] = _clamp(latent_skill - 0.04 + rng.gauss(0.0, profile.volatility))

    observations = []
    if status != "correct" and missing_prerequisite:
        observations.append({
            "code": "missing_prerequisite",
            "related_competency_id": missing_prerequisite,
            "observer_confidence": 0.90,
        })

    return {
        "event_id": f"{profile.name}-s{stage_index+1}-n{session_index+1}-i{item_index+1}-{competency_id}",
        "competency_id": competency_id,
        "observed_at": f"2030-{stage_index+1:02d}-{session_index+1:02d}T10:{item_index:02d}:00+02:00",
        "outcome": outcome,
        "support": {"level": support},
        "task": {"context_familiarity": context},
        "error_observations": observations,
        "tags": [f"stage:{stage_index+1}", f"session_action:{action}"],
    }


def recovery_depth_hint(competency_id: str, profile: EightYearProfile) -> int:
    if competency_id == profile.deep_gap_prerequisite:
        return 2
    if competency_id == profile.gap_prerequisite:
        return 1
    return 0


def _child_gap(profile: EightYearProfile, stage_number: int, competency_id: str, resolved: set[str]) -> str | None:
    if profile.gap_stage != stage_number:
        return None
    if competency_id == profile.targets[stage_number - 1] and profile.gap_prerequisite not in resolved:
        return profile.gap_prerequisite
    if competency_id == profile.gap_prerequisite and profile.deep_gap_prerequisite and profile.deep_gap_prerequisite not in resolved:
        return profile.deep_gap_prerequisite
    return None


def _oracle_root(profile: EightYearProfile, stage_number: int, skill: float, unresolved_gap: bool) -> str:
    if unresolved_gap:
        return "recover"
    if profile.profile_kind == "support_dependent":
        return "consolidate"
    transfer = skill + profile.transfer_offset
    if skill >= 0.88 and transfer >= 0.76:
        return "extend"
    if skill >= 0.74:
        return "advance"
    return "consolidate"


def _gain(action: str, base: float) -> float:
    if action in {"recover", "consolidate"}:
        return base
    if action == "reassess":
        return base * 0.22
    return 0.0


def run_profile_8y(
    profile: EightYearProfile,
    policy: dict[str, Any],
    *,
    seed: int,
    max_sessions_per_stage: int = 8,
) -> dict[str, Any]:
    rng = random.Random(seed)
    events: list[dict[str, Any]] = []
    resolved: set[str] = set()
    completed_stages = 0
    trace: list[dict[str, Any]] = []
    metrics = {
        "premature_advance": 0,
        "false_recovery": 0,
        "reassess_loops": 0,
        "stagnated_stages": 0,
        "cross_stage_recovery_detected": 0,
        "cross_stage_returned": 0,
        "deep_recovery_detected": 0,
        "deep_recovery_returned": 0,
        "support_dependent_early_advance": 0,
    }

    gap_skills: dict[str, float] = {}
    if profile.gap_prerequisite and profile.gap_skill is not None:
        gap_skills[profile.gap_prerequisite] = profile.gap_skill
    if profile.deep_gap_prerequisite and profile.deep_gap_skill is not None:
        gap_skills[profile.deep_gap_prerequisite] = profile.deep_gap_skill

    for stage_index, root_target in enumerate(profile.targets):
        stage_number = stage_index + 1
        root_skill = _clamp(profile.initial_skill + profile.yearly_gain * stage_index)
        if profile.gap_stage == stage_number and profile.gap_prerequisite not in resolved:
            root_skill = min(root_skill, 0.48)
        skills = {root_target: root_skill, **gap_skills}
        stack = start_objective(root_target)
        action = "reassess"
        consecutive_reassess = 0
        stage_completed = False
        saw_cross_stage_recovery = False
        saw_deep_recovery = False

        for session_index in range(max_sessions_per_stage):
            current = current_objective(stack)
            depth = recovery_depth(stack)
            latent = skills.get(current, root_skill)
            missing = _child_gap(profile, stage_number, current, resolved)
            effective_latent = min(latent, 0.46) if missing else latent

            for item_index in range(6):
                events.append(_event(
                    profile,
                    current,
                    effective_latent,
                    stage_index=stage_index,
                    session_index=session_index,
                    item_index=item_index,
                    action=action,
                    rng=rng,
                    missing_prerequisite=missing,
                ))

            gain = profile.recovery_gain if depth else profile.learning_gain
            skills[current] = _clamp(latent + _gain(action, gain))
            state = calibrated_state(current, events, policy)
            choice = decide(
                state,
                policy,
                current_target_id=current,
                suggested_next_id="synthetic.next",
                recovery_depth=depth,
            )
            decision = choice.action

            if decision == "reassess":
                consecutive_reassess += 1
                if consecutive_reassess >= 3:
                    metrics["reassess_loops"] += 1
            else:
                consecutive_reassess = 0

            unresolved_root_gap = _child_gap(profile, stage_number, root_target, resolved) is not None
            expected = _oracle_root(profile, stage_number, skills[root_target], unresolved_root_gap)
            if depth == 0 and decision in {"advance", "extend"} and expected not in {"advance", "extend"}:
                metrics["premature_advance"] += 1
            if depth == 0 and decision == "recover" and not unresolved_root_gap:
                metrics["false_recovery"] += 1
            if profile.profile_kind == "support_dependent" and stage_number <= 3 and depth == 0 and decision in {"advance", "extend"}:
                metrics["support_dependent_early_advance"] += 1

            trace.append({
                "stage": stage_number,
                "root": root_target,
                "current": current,
                "depth": depth,
                "session": session_index + 1,
                "action_used": action,
                "decision": decision,
                "state_status": state.get("status"),
                "state_confidence": state.get("confidence"),
            })

            if depth > 0 and decision in {"advance", "extend"}:
                resolved.add(current)
                stack = complete_current(stack)
                parent = current_objective(stack)
                if parent in skills:
                    skills[parent] = _clamp(skills[parent] + 0.10)
                action = "reassess" if policy.get("post_recovery_reassess", True) else "consolidate"
                if recovery_depth(stack) == 0:
                    if saw_cross_stage_recovery:
                        metrics["cross_stage_returned"] += 1
                    if saw_deep_recovery:
                        metrics["deep_recovery_returned"] += 1
                continue

            if decision == "recover" and choice.recovery_competency_id:
                try:
                    stack = push_recovery(
                        stack,
                        choice.recovery_competency_id,
                        reason=choice.rationale,
                        max_depth=int(policy["max_recovery_depth"]),
                    )
                    if stage_number >= 4 and ".us." not in choice.recovery_competency_id:
                        saw_cross_stage_recovery = True
                        metrics["cross_stage_recovery_detected"] = 1
                    if recovery_depth(stack) >= 2:
                        saw_deep_recovery = True
                        metrics["deep_recovery_detected"] = 1
                    action = "recover"
                    continue
                except ValueError:
                    action = "reassess"
                    continue

            if depth == 0 and decision in {"advance", "extend"}:
                stage_completed = True
                completed_stages += 1
                break

            action = decision

        if not stage_completed:
            metrics["stagnated_stages"] += 1
            break

    return {
        "profile": profile.name,
        "profile_kind": profile.profile_kind,
        "subject": profile.subject,
        "completed_stages": completed_stages,
        "metrics": metrics,
        "trace": trace,
    }


def run_suite_8y(
    policy: dict[str, Any],
    *,
    seeds: int = 40,
    max_sessions_per_stage: int = 8,
) -> dict[str, Any]:
    runs = [
        run_profile_8y(profile, policy, seed=90_000 + seed, max_sessions_per_stage=max_sessions_per_stage)
        for seed in range(seeds)
        for profile in PROFILES_8Y
    ]
    total = len(runs)
    strong = [run for run in runs if run["profile_kind"] == "strong"]
    typical = [run for run in runs if run["profile_kind"] == "typical"]
    gaps = [run for run in runs if run["profile_kind"] == "cross_stage_gap"]
    support = [run for run in runs if run["profile_kind"] == "support_dependent"]

    def rate(rows, predicate):
        return round(sum(1 for row in rows if predicate(row)) / max(1, len(rows)), 4)

    metrics = {
        "premature_advance_per_run": round(sum(r["metrics"]["premature_advance"] for r in runs) / total, 4),
        "false_recovery_per_run": round(sum(r["metrics"]["false_recovery"] for r in runs) / total, 4),
        "reassess_loop_per_run": round(sum(r["metrics"]["reassess_loops"] for r in runs) / total, 4),
        "stagnated_stage_per_run": round(sum(r["metrics"]["stagnated_stages"] for r in runs) / total, 4),
        "strong_complete_8y_rate": rate(strong, lambda r: r["completed_stages"] == 8),
        "typical_complete_8y_rate": rate(typical, lambda r: r["completed_stages"] == 8),
        "cross_stage_recovery_detect_rate": rate(gaps, lambda r: r["metrics"]["cross_stage_recovery_detected"] == 1),
        "cross_stage_return_rate": rate(gaps, lambda r: r["metrics"]["cross_stage_returned"] >= 1),
        "deep_recovery_detect_rate": rate(gaps, lambda r: r["metrics"]["deep_recovery_detected"] == 1),
        "deep_recovery_return_rate": rate(gaps, lambda r: r["metrics"]["deep_recovery_returned"] >= 1),
        "support_dependency_guard_rate": rate(support, lambda r: r["metrics"]["support_dependent_early_advance"] == 0),
        "mean_completed_stages": round(sum(r["completed_stages"] for r in runs) / total, 4),
    }
    return {
        "version": "0.9",
        "synthetic_only": True,
        "profiles": len(PROFILES_8Y),
        "seeds_per_profile": seeds,
        "total_runs": total,
        "stages_per_path": 8,
        "max_sessions_per_stage": max_sessions_per_stage,
        "metrics": metrics,
    }
