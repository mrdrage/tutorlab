from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any

from engine.learning_snapshot import competency_state, with_objective_stack
from engine.path_selector import select_target, suggested_successor
from engine.decision_bridge import route
from engine.session_dispatch import dispatch
from engine.stack_bridge import ensure_stack
from engine.result_transition import transition
from engine.session_engine import student_view

ROOT = Path(__file__).resolve().parents[1]
POLICY_PATH = ROOT / "config" / "adaptive-policy.json"

ALLOWED_INTENTS = {"continue", "lesson", "practice", "assessment"}


def load_policy() -> dict[str, Any]:
    return json.loads(POLICY_PATH.read_text(encoding="utf-8"))


def _validate_request(request: dict[str, Any]) -> None:
    subject = request.get("subject")
    intent = request.get("intent")
    if not subject:
        raise ValueError("subject is required")
    if intent not in ALLOWED_INTENTS:
        raise ValueError("unsupported intent")
    duration = request.get("duration_minutes")
    if duration is not None and not 10 <= int(duration) <= 120:
        raise ValueError("duration_minutes outside supported range")
    band = request.get("max_challenge_band")
    if band is not None and not 1 <= int(band) <= 5:
        raise ValueError("max_challenge_band outside supported range")


def _requested_action(intent: str, adaptive_action: str, selection_reason: str) -> str:
    if selection_reason == "known_prerequisite_gap":
        return "recover"
    if selection_reason == "prerequisite_needs_evidence":
        return "reassess"
    if intent == "assessment":
        return "reassess"
    if intent == "practice" and adaptive_action in {"advance", "extend"}:
        return "consolidate"
    return adaptive_action


def plan(snapshot: dict[str, Any], request: dict[str, Any], *, seed: int = 1) -> dict[str, Any]:
    _validate_request(request)
    policy = load_policy()
    subject = str(request["subject"])
    requested_target = request.get("target_competency_id")

    selection = select_target(snapshot, subject, requested_target_id=requested_target)
    working_target = selection["working_target_id"]
    state = competency_state(snapshot, subject, working_target)
    successor = suggested_successor(snapshot, subject, working_target)
    existing_stack = snapshot["subjects"][subject].get("objective_stack")
    stack = ensure_stack(existing_stack, selection, int(policy["max_recovery_depth"]))
    depth = sum(1 for frame in stack.get("frames", []) if frame.get("kind") == "recovery")

    decision = route(
        state,
        policy,
        target=working_target,
        successor=successor,
        depth=depth,
    )
    action = _requested_action(str(request["intent"]), decision.action, selection["reason"])

    preferences = snapshot.get("preferences", {})
    duration = int(request.get("duration_minutes") or preferences.get("default_duration_minutes", 40))
    max_band = int(request.get("max_challenge_band") or preferences.get("max_challenge_band", 5))
    history = list(snapshot.get("recent_activity", {}).get("fingerprints", []))

    generated = dispatch(
        working_target,
        action,
        selection["root_target_id"],
        seed=seed,
        duration_minutes=duration,
        max_challenge_band=max_band,
        history_fingerprints=history,
    )
    if generated["status"] != "ok":
        return {
            "status": generated["status"],
            "warning": generated["warning"],
            "selection": selection,
            "decision": {
                "action": action,
                "rationale": decision.rationale,
            },
            "session": None,
            "student_session": None,
            "objective_stack": stack,
        }

    session = generated["session"]
    return {
        "status": "ok",
        "warning": None,
        "selection": selection,
        "decision": {
            "action": action,
            "adaptive_action": decision.action,
            "rationale": decision.rationale,
            "selection_reason": selection["reason"],
        },
        "objective_stack": stack,
        "session": session,
        "student_session": student_view(session) if request.get("student_view", True) else None,
    }


def persist_planned_stack(snapshot: dict[str, Any], subject: str, plan_result: dict[str, Any]) -> dict[str, Any]:
    if plan_result.get("status") != "ok":
        return deepcopy(snapshot)
    return with_objective_stack(snapshot, subject, plan_result["objective_stack"])


def record_result(
    snapshot: dict[str, Any],
    subject: str,
    session: dict[str, Any],
    session_result: dict[str, Any],
) -> dict[str, Any]:
    policy = load_policy()
    return transition(snapshot, subject, session, session_result, policy)


def hub_plan(exchange: dict[str, Any], *, seed: int = 1) -> dict[str, Any]:
    if str(exchange.get("version")) != "1.0":
        raise ValueError("unsupported exchange version")
    snapshot = exchange["learning_snapshot"]
    request = exchange["request"]
    result = plan(snapshot, request, seed=seed)
    return {
        "version": "1.0",
        "student_ref": deepcopy(exchange["student_ref"]),
        "plan": result,
    }


def hub_transition(exchange: dict[str, Any]) -> dict[str, Any]:
    if str(exchange.get("version")) != "1.0":
        raise ValueError("unsupported exchange version")
    result = exchange.get("session_result")
    if not result:
        raise ValueError("session_result is required")
    metadata = exchange.get("metadata", {})
    subject = metadata.get("subject")
    session = metadata.get("session")
    if not subject or not session:
        raise ValueError("metadata.subject and metadata.session are required")
    outcome = record_result(exchange["learning_snapshot"], str(subject), session, result)
    return {
        "version": "1.0",
        "student_ref": deepcopy(exchange["student_ref"]),
        "transition": outcome,
    }
