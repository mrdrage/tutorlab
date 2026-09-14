from __future__ import annotations

import json
from dataclasses import asdict, is_dataclass
from pathlib import Path
from typing import Any

from engine.curriculum_access import load_competency
from engine.learning_snapshot import competency_state, with_objective_stack
from engine.path_selector import select_target, suggested_successor
from engine.plan_kernel import resolve
from engine.result_transition import transition
from engine.session_dispatch import dispatch
from engine.session_engine import student_view
from engine.stack_bridge import ensure_stack

ROOT = Path(__file__).resolve().parents[1]
POLICY_PATH = ROOT / "config" / "adaptive-policy.json"

SUBJECTS = {"mathematics", "english", "italian", "french", "spanish"}
INTENTS = {"adaptive", "practice", "assessment", "diagnostic"}
OUTPUTS = {"both", "tutor", "student"}


def load_policy() -> dict[str, Any]:
    return json.loads(POLICY_PATH.read_text(encoding="utf-8"))


def _decision_payload(decision: Any) -> dict[str, Any] | None:
    if decision is None:
        return None
    if is_dataclass(decision):
        return asdict(decision)
    if isinstance(decision, dict):
        return dict(decision)
    return {"value": str(decision)}


def normalize_request(snapshot: dict[str, Any], request: dict[str, Any]) -> dict[str, Any]:
    if request.get("version") != "1.0-rc1":
        raise ValueError("unsupported tutor request version")

    subject = str(request.get("subject", ""))
    if subject not in SUBJECTS:
        raise ValueError("unsupported subject")
    if subject not in snapshot.get("subjects", {}):
        raise ValueError("subject missing from learning snapshot")

    preferences = snapshot.get("preferences", {})
    duration = int(request.get("duration_minutes", preferences.get("default_duration_minutes", 40)))
    if not 10 <= duration <= 120:
        raise ValueError("duration_minutes must be between 10 and 120")

    max_band = int(request.get("max_challenge_band", preferences.get("max_challenge_band", 5)))
    if not 1 <= max_band <= 5:
        raise ValueError("max_challenge_band must be between 1 and 5")

    intent = str(request.get("intent", "adaptive"))
    if intent not in INTENTS:
        raise ValueError("unsupported tutor intent")

    output = str(request.get("output", "both"))
    if output not in OUTPUTS:
        raise ValueError("unsupported output mode")

    target = request.get("requested_target_id")
    if target is not None and not str(target).strip():
        raise ValueError("requested_target_id cannot be empty")

    seed = int(request.get("seed", 1))
    if seed < 0:
        raise ValueError("seed must be non-negative")

    return {
        "version": "1.0-rc1",
        "subject": subject,
        "requested_target_id": str(target) if target is not None else None,
        "duration_minutes": duration,
        "seed": seed,
        "intent": intent,
        "max_challenge_band": max_band,
        "output": output,
    }


def _direct_plan(intent: str, target: str, stack: dict[str, Any]) -> dict[str, Any]:
    action = "consolidate" if intent == "practice" else "reassess"
    label = {
        "practice": "tutor_requested_practice",
        "assessment": "tutor_requested_assessment",
        "diagnostic": "tutor_requested_diagnostic",
    }[intent]
    return {
        "kind": "direct",
        "target": target,
        "action": action,
        "stack": stack,
        "decision": None,
        "rationale": label,
    }


def _adaptive_plan(snapshot: dict[str, Any], subject: str, selection: dict[str, Any], stack: dict[str, Any], policy: dict[str, Any]) -> dict[str, Any]:
    current = stack["frames"][-1]["competency_id"]
    resolved = resolve(
        selection,
        stack,
        competency_state(snapshot, subject, current),
        suggested_successor(snapshot, subject, current),
        policy,
    )
    decision = _decision_payload(resolved.get("decision"))

    if resolved["kind"] == "return_to":
        return {
            "kind": "return_to",
            "target": resolved["target"],
            "action": resolved.get("next_action") or "reassess",
            "stack": resolved["stack"],
            "decision": decision,
            "rationale": "resume_suspended_target_after_recovery",
        }

    return {
        "kind": resolved["kind"],
        "target": resolved["target"],
        "action": resolved["action"],
        "stack": resolved["stack"],
        "decision": decision,
        "rationale": (decision or {}).get("rationale", selection.get("reason", "adaptive_plan")),
    }


def _brief(request: dict[str, Any], selection: dict[str, Any], plan: dict[str, Any], session: dict[str, Any]) -> dict[str, Any]:
    competency = load_competency(plan["target"])
    tasks = [task for phase in session.get("phases", []) for task in phase.get("tasks", [])]
    return {
        "subject": request["subject"],
        "intent": request["intent"],
        "root_target_id": selection["root_target_id"],
        "working_target_id": plan["target"],
        "working_target_title": competency.get("title", plan["target"]),
        "action": plan["action"],
        "rationale": plan["rationale"],
        "duration_minutes": session["duration_minutes"],
        "challenge_band": session["challenge_band"],
        "phase_count": len(session.get("phases", [])),
        "task_count": len(tasks),
    }


def prepare_tutor_package(snapshot: dict[str, Any], request: dict[str, Any], *, policy: dict[str, Any] | None = None) -> dict[str, Any]:
    policy = policy or load_policy()
    normalized = normalize_request(snapshot, request)
    subject = normalized["subject"]

    selection = select_target(snapshot, subject, normalized["requested_target_id"])
    stack = ensure_stack(
        snapshot["subjects"][subject].get("objective_stack"),
        selection,
        int(policy["max_recovery_depth"]),
    )
    current = stack["frames"][-1]["competency_id"]

    if normalized["intent"] == "adaptive":
        plan = _adaptive_plan(snapshot, subject, selection, stack, policy)
    else:
        plan = _direct_plan(normalized["intent"], current, stack)

    stack = plan["stack"]
    sent = dispatch(
        plan["target"],
        plan["action"],
        stack["root_target_id"],
        seed=normalized["seed"],
        duration_minutes=normalized["duration_minutes"],
        max_challenge_band=normalized["max_challenge_band"],
        history_fingerprints=snapshot.get("recent_activity", {}).get("fingerprints", []),
    )

    package = {
        "version": "1.0-rc1",
        "status": sent["status"],
        "warning": sent.get("warning"),
        "request": normalized,
        "selection": selection,
        "objective_stack": stack,
        "plan": {
            "kind": plan["kind"],
            "target": plan["target"],
            "action": plan["action"],
            "rationale": plan["rationale"],
            "decision": plan.get("decision"),
        },
        "snapshot_patch": {"subject": subject, "objective_stack": stack},
        "session": sent.get("session"),
        "views": {"tutor": None, "student": None},
    }

    if sent["status"] != "ok" or not sent.get("session"):
        return package

    session = sent["session"]
    if normalized["output"] in {"both", "tutor"}:
        package["views"]["tutor"] = {"brief": _brief(normalized, selection, plan, session), "session": session}
    if normalized["output"] in {"both", "student"}:
        package["views"]["student"] = student_view(session)
    return package


def apply_plan_patch(snapshot: dict[str, Any], package: dict[str, Any]) -> dict[str, Any]:
    if package.get("version") != "1.0-rc1":
        raise ValueError("unsupported tutor package version")
    patch = package["snapshot_patch"]
    return with_objective_stack(snapshot, patch["subject"], patch["objective_stack"])


def complete_tutor_session(
    snapshot: dict[str, Any],
    package: dict[str, Any],
    result: dict[str, Any],
    *,
    policy: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if package.get("status") != "ok" or not package.get("session"):
        raise ValueError("cannot complete a package without an executable session")
    if package.get("version") != "1.0-rc1":
        raise ValueError("unsupported tutor package version")

    session = package["session"]
    if result.get("session_id") != session.get("session_id"):
        raise ValueError("session result does not match tutor package")

    subject = package["request"]["subject"]
    if session.get("subject") != subject:
        raise ValueError("session subject does not match tutor package")

    policy = policy or load_policy()
    planned_snapshot = apply_plan_patch(snapshot, package)
    moved = transition(planned_snapshot, subject, session, result, policy)
    next_step = moved["next_step"]
    return {
        "version": "1.0-rc1",
        "subject": subject,
        "session_id": session["session_id"],
        "snapshot_update": moved["snapshot_update"],
        "next_step": next_step,
        "pending_task_ids": moved["pending_task_ids"],
        "evidence_events": moved["evidence_events"],
        "tutor_summary": {
            "evidence_count": len(moved["evidence_events"]),
            "pending_count": len(moved["pending_task_ids"]),
            "next_action": next_step["action"],
            "next_target": next_step["target"],
        },
    }
