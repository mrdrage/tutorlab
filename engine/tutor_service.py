from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any

from engine.learning_snapshot import competency_state, with_objective_stack
from engine.path_selector import select_target, suggested_successor
from engine.decision_bridge import route
from engine.stack_bridge import ensure_stack
from engine.result_transition import transition
from engine.session_engine import build_session, student_view
from engine.task_families import can_generate

ROOT = Path(__file__).resolve().parents[1]
POLICY_PATH = ROOT / "config" / "adaptive-policy.json"
DEFAULT_BANDS={"recover":1,"consolidate":2,"advance":2,"extend":4,"reassess":2}
ALLOWED_INTENTS = {"continue", "lesson", "practice", "assessment"}
ALLOWED_SUBJECTS = {"mathematics", "english", "italian", "french", "spanish"}
ALLOWED_REQUEST_FIELDS = {"subject","intent","target_competency_id","duration_minutes","max_challenge_band","quantity_hint","student_view","notes"}


def load_policy() -> dict[str, Any]:
    return json.loads(POLICY_PATH.read_text(encoding="utf-8"))


def _bounded_int(value: Any, low: int, high: int, field: str) -> None:
    if value is None:
        return
    if isinstance(value,bool) or not isinstance(value,int) or not low <= value <= high:
        raise ValueError(f"{field} outside supported range")


def _validate_request(request: dict[str, Any]) -> None:
    if not isinstance(request,dict):
        raise ValueError("request must be an object")
    unknown=set(request)-ALLOWED_REQUEST_FIELDS
    if unknown:
        raise ValueError(f"unsupported request fields: {sorted(unknown)}")
    subject = request.get("subject")
    intent = request.get("intent")
    if subject not in ALLOWED_SUBJECTS:
        raise ValueError("unsupported subject")
    if intent not in ALLOWED_INTENTS:
        raise ValueError("unsupported intent")
    target=request.get("target_competency_id")
    if target is not None and (not isinstance(target,str) or not target):
        raise ValueError("invalid target_competency_id")
    _bounded_int(request.get("duration_minutes"),10,120,"duration_minutes")
    _bounded_int(request.get("max_challenge_band"),1,5,"max_challenge_band")
    _bounded_int(request.get("quantity_hint"),1,30,"quantity_hint")
    if "student_view" in request and not isinstance(request["student_view"],bool):
        raise ValueError("student_view must be boolean")
    notes=request.get("notes")
    if notes is not None and (not isinstance(notes,str) or len(notes)>500):
        raise ValueError("invalid notes")


def _validate_exchange(exchange: dict[str, Any], *, require_request: bool = False, require_result: bool = False) -> None:
    if not isinstance(exchange,dict):
        raise ValueError("exchange must be an object")
    if str(exchange.get("version")) != "1.0":
        raise ValueError("unsupported exchange version")
    student_ref=exchange.get("student_ref") or {}
    if not isinstance(student_ref,dict) or not isinstance(student_ref.get("external_id"),str) or not student_ref.get("external_id"):
        raise ValueError("student_ref.external_id is required")
    if not isinstance(exchange.get("learning_snapshot"),dict):
        raise ValueError("learning_snapshot is required")
    if require_request and not isinstance(exchange.get("request"),dict):
        raise ValueError("request is required")
    if require_result and not isinstance(exchange.get("session_result"),dict):
        raise ValueError("session_result is required")


def _requested_action(intent: str, adaptive_action: str, selection_reason: str) -> str:
    if intent == "assessment":
        return "reassess"
    if selection_reason == "known_prerequisite_gap":
        return "recover"
    if selection_reason == "prerequisite_needs_evidence":
        return "reassess"
    if intent == "practice" and adaptive_action in {"advance", "extend"}:
        return "consolidate"
    return adaptive_action


def _generate(working_target: str, action: str, root_target: str, *, seed: int, duration: int, max_band: int, quantity_hint: int | None, history: list[str]):
    if not can_generate(working_target):
        return {"status":"needs_review","warning":f"task_family_not_available:{working_target}","session":None}
    session=build_session(
        working_target,
        action,
        original_target_id=root_target,
        challenge_band=min(DEFAULT_BANDS[action],max_band),
        duration_minutes=duration,
        quantity_hint=quantity_hint,
        seed=seed,
        history_fingerprints=history,
    )
    return {"status":"ok","warning":None,"session":session}


def plan(snapshot: dict[str, Any], request: dict[str, Any], *, seed: int = 1) -> dict[str, Any]:
    if not isinstance(snapshot,dict):
        raise ValueError("learning snapshot must be an object")
    _validate_request(request)
    policy = load_policy()
    subject = request["subject"]
    if subject not in snapshot.get("subjects", {}):
        raise ValueError("subject missing from learning snapshot")
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
    action = _requested_action(request["intent"], decision.action, selection["reason"])

    preferences = snapshot.get("preferences", {})
    duration = request.get("duration_minutes") or preferences.get("default_duration_minutes", 40)
    max_band = request.get("max_challenge_band") or preferences.get("max_challenge_band", 5)
    quantity_hint = request.get("quantity_hint")
    history = list(snapshot.get("recent_activity", {}).get("fingerprints", []))

    generated = _generate(
        working_target,
        action,
        selection["root_target_id"],
        seed=seed,
        duration=int(duration),
        max_band=int(max_band),
        quantity_hint=quantity_hint,
        history=history,
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
    if subject not in ALLOWED_SUBJECTS or subject not in snapshot.get("subjects", {}):
        raise ValueError("invalid transition subject")
    if session.get("subject") != subject:
        raise ValueError("session subject does not match transition subject")
    policy = load_policy()
    return transition(snapshot, subject, session, session_result, policy)


def hub_plan(exchange: dict[str, Any], *, seed: int = 1) -> dict[str, Any]:
    _validate_exchange(exchange,require_request=True)
    snapshot = exchange["learning_snapshot"]
    request = exchange["request"]
    result = plan(snapshot, request, seed=seed)
    return {
        "version": "1.0",
        "student_ref": deepcopy(exchange["student_ref"]),
        "plan": result,
    }


def hub_transition(exchange: dict[str, Any]) -> dict[str, Any]:
    _validate_exchange(exchange,require_result=True)
    result = exchange["session_result"]
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
