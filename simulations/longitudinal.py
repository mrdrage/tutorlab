from __future__ import annotations

import random
from typing import Any

from engine.adaptive_engine import decide
from engine.reliability_state import calibrated_state
from simulations.profiles import PROFILES, SyntheticProfile


def _clamp(value: float) -> float:
    return max(0.0, min(1.0, value))


def _support_level(rng: random.Random, dependence: float, index: int) -> str:
    if dependence >= 0.7:
        return ("worked_support", "structured_prompt", "light_prompt", "structured_prompt")[index % 4]
    if dependence >= 0.3:
        return ("structured_prompt", "light_prompt", "none", "light_prompt")[index % 4]
    return ("light_prompt", "none", "none", "none")[index % 4]


def _event(
    profile: SyntheticProfile,
    competency_id: str,
    latent_skill: float,
    session_index: int,
    item_index: int,
    rng: random.Random,
) -> dict[str, Any]:
    dependence = profile.support_dependence if competency_id == profile.target else max(0.0, profile.support_dependence - 0.2)
    support = _support_level(rng, dependence, item_index)
    boost = {"none": 0.0, "light_prompt": 0.05, "structured_prompt": 0.12, "worked_support": 0.20}[support]
    probability = _clamp(latent_skill + boost + rng.gauss(0.0, profile.volatility))
    draw = rng.random()
    if draw < probability - 0.08:
        status = "correct"
    elif draw < probability + 0.08:
        status = "partially_correct"
    else:
        status = "incorrect"

    outcome: dict[str, Any] = {"status": status}
    context = "familiar"
    if item_index == 3:
        context = "near_transfer"
        transfer_base = profile.transfer_skill if competency_id == profile.target and profile.transfer_skill is not None else latent_skill - 0.05
        outcome["transfer_success"] = _clamp(transfer_base + rng.gauss(0.0, profile.volatility))
    if item_index == 2:
        outcome["explanation_quality"] = _clamp(latent_skill - 0.05 + rng.gauss(0.0, profile.volatility))

    observations = []
    if status != "correct" and competency_id == profile.target and profile.error_code:
        observations.append({
            "code": profile.error_code,
            "related_competency_id": profile.prerequisite if profile.error_code == "missing_prerequisite" else None,
            "observer_confidence": 0.82 if profile.error_code == "missing_prerequisite" else 0.78,
        })

    tags = []
    if latent_skill > 0.8 and item_index == 1:
        tags.append("fluency_ok")
    elif latent_skill < 0.6 and item_index == 1:
        tags.append("fluency_slow")

    return {
        "event_id": f"{profile.name}-{session_index}-{item_index}-{competency_id}",
        "competency_id": competency_id,
        "observed_at": f"2026-09-{1 + session_index:02d}T10:{item_index:02d}:00+02:00",
        "outcome": outcome,
        "support": {"level": support},
        "task": {"context_familiarity": context},
        "error_observations": observations,
        "tags": tags,
    }


def _oracle(profile: SyntheticProfile, target_skill: float, prerequisite_skill: float | None, in_recovery: bool) -> str:
    if in_recovery:
        return "return" if prerequisite_skill is not None and prerequisite_skill >= 0.72 else "consolidate"
    if profile.profile_kind == "prerequisite_gap" and prerequisite_skill is not None and prerequisite_skill < 0.55:
        return "recover"
    if profile.profile_kind == "support_dependent":
        return "consolidate"
    if profile.profile_kind in {"conceptual_gap", "strategy_gap"} and target_skill < 0.68:
        return "consolidate"
    if target_skill >= 0.88 and (profile.transfer_skill or target_skill) >= 0.78:
        return "extend"
    if target_skill >= 0.74:
        return "advance"
    return "consolidate"


def run_profile(profile: SyntheticProfile, policy: dict[str, Any], *, seed: int, sessions: int = 12) -> dict[str, Any]:
    rng = random.Random(seed)
    target_skill = profile.target_skill
    prerequisite_skill = profile.prerequisite_skill
    events: list[dict[str, Any]] = []
    in_recovery = False
    recovery_depth = 0
    next_session_action = "reassess"
    actions: list[str] = []
    decisions: list[str] = []

    metrics = {
        "premature_advance": 0,
        "missed_recovery": 0,
        "false_recovery": 0,
        "recovery_returns": 0,
        "reassess_loops": 0,
    }
    consecutive_reassess = 0

    for session_index in range(sessions):
        competency_id = profile.prerequisite if in_recovery else profile.target
        latent = prerequisite_skill if in_recovery else target_skill
        if competency_id is None or latent is None:
            break

        actions.append(next_session_action)
        for item_index in range(4):
            events.append(_event(profile, competency_id, latent, session_index, item_index, rng))

        if in_recovery:
            if next_session_action in {"recover", "consolidate"}:
                prerequisite_skill = _clamp(float(prerequisite_skill) + profile.prerequisite_gain)
            elif next_session_action == "reassess":
                prerequisite_skill = _clamp(float(prerequisite_skill) + profile.prerequisite_gain * 0.25)
        else:
            if next_session_action == "consolidate":
                target_skill = _clamp(target_skill + profile.learning_gain)
            elif next_session_action == "reassess":
                target_skill = _clamp(target_skill + profile.learning_gain * 0.12)

        state = calibrated_state(competency_id, events, policy)
        choice = decide(
            state,
            policy,
            current_target_id=competency_id,
            suggested_next_id="synthetic.next",
            recovery_depth=recovery_depth,
        )
        decision = choice.action
        decisions.append(decision)
        expected = _oracle(profile, target_skill, prerequisite_skill, in_recovery)

        if decision == "reassess":
            consecutive_reassess += 1
            if consecutive_reassess >= 3:
                metrics["reassess_loops"] += 1
        else:
            consecutive_reassess = 0

        if in_recovery:
            if decision in {"advance", "extend"}:
                metrics["recovery_returns"] += 1
                in_recovery = False
                recovery_depth = 0
                target_skill = _clamp(target_skill + 0.08)
                next_session_action = "reassess" if policy.get("post_recovery_reassess", True) else "consolidate"
            else:
                next_session_action = decision
            continue

        if decision == "advance" and expected not in {"advance", "extend"}:
            metrics["premature_advance"] += 1
        if expected == "recover" and decision not in {"recover", "reassess"}:
            metrics["missed_recovery"] += 1
        if decision == "recover" and expected != "recover":
            metrics["false_recovery"] += 1

        if decision == "recover" and profile.prerequisite:
            in_recovery = True
            recovery_depth = 1
            next_session_action = "recover"
        else:
            next_session_action = decision

    return {
        "profile": profile.name,
        "profile_kind": profile.profile_kind,
        "subject": profile.subject,
        "actions": actions,
        "decisions": decisions,
        "metrics": metrics,
        "final_target_skill": round(target_skill, 4),
        "final_prerequisite_skill": round(prerequisite_skill, 4) if prerequisite_skill is not None else None,
    }


def run_suite(policy: dict[str, Any], *, seeds: int = 50, sessions: int = 12) -> dict[str, Any]:
    runs = [
        run_profile(profile, policy, seed=10_000 + seed, sessions=sessions)
        for seed in range(seeds)
        for profile in PROFILES
    ]
    total = len(runs)
    gap_runs = [run for run in runs if run["profile_kind"] == "prerequisite_gap"]
    strong_runs = [run for run in runs if run["profile_kind"] == "strong"]
    support_runs = [run for run in runs if run["profile_kind"] == "support_dependent"]

    premature = sum(run["metrics"]["premature_advance"] for run in runs)
    loops = sum(run["metrics"]["reassess_loops"] for run in runs)
    false_recovery = sum(run["metrics"]["false_recovery"] for run in runs)

    recovery_detected = sum("recover" in run["decisions"][:5] for run in gap_runs)
    recovery_returned = sum(run["metrics"]["recovery_returns"] >= 1 for run in gap_runs)
    strong_progress = sum(any(action in {"advance", "extend"} for action in run["decisions"][:5]) for run in strong_runs)
    support_guard = sum(not any(action in {"advance", "extend"} for action in run["decisions"][:8]) for run in support_runs)

    return {
        "version": "0.5",
        "synthetic_only": True,
        "profiles": len(PROFILES),
        "seeds_per_profile": seeds,
        "total_runs": total,
        "sessions_per_run": sessions,
        "metrics": {
            "premature_advance_per_run": round(premature / total, 4),
            "false_recovery_per_run": round(false_recovery / total, 4),
            "reassess_loop_per_run": round(loops / total, 4),
            "recovery_detect_rate": round(recovery_detected / max(1, len(gap_runs)), 4),
            "recovery_return_rate": round(recovery_returned / max(1, len(gap_runs)), 4),
            "strong_progress_by_session_5": round(strong_progress / max(1, len(strong_runs)), 4),
            "support_dependency_guard_rate": round(support_guard / max(1, len(support_runs)), 4),
        },
    }
