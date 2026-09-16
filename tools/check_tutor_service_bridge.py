#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path

from engine.learning_snapshot import with_objective_stack
from examples.learning_snapshot.synthetic_cases import mathematics_case

ROOT = Path(__file__).resolve().parents[1]
BRIDGE = ROOT / "tools" / "tutor_service_bridge.py"
BRIDGE_VERSION = "1.0"


def call_raw(raw: str):
    completed = subprocess.run(
        [sys.executable, str(BRIDGE)],
        cwd=ROOT,
        input=raw,
        text=True,
        capture_output=True,
        check=False,
    )
    body = json.loads(completed.stdout)
    assert completed.stderr == "", completed.stderr
    assert body["bridge_version"] == BRIDGE_VERSION
    return completed.returncode, body


def call(request):
    return call_raw(json.dumps(request, ensure_ascii=False))


def envelope(operation, payload, **extra):
    request = {
        "bridge_version": BRIDGE_VERSION,
        "operation": operation,
        "payload": payload,
    }
    request.update(extra)
    return request


def _all_correct_result(session):
    responses = []
    for phase in session.get("phases", []):
        for task in phase.get("tasks", []):
            responses.append(
                {
                    "task_id": task["task_id"],
                    "response": "synthetic-correct-response",
                    "status": "correct",
                    "score": 1.0,
                    "support_used": "none",
                    "transfer_success": 1.0
                    if phase["kind"] in {"transfer", "transfer_probe", "challenge"}
                    else None,
                    "explanation_quality": 0.9 if phase["kind"] == "explanation" else None,
                }
            )
    return {
        "version": "0.1",
        "session_id": session["session_id"],
        "completed_at": datetime.now(timezone.utc).isoformat(),
        "completion_status": "completed",
        "responses": responses,
    }


def _assert_protocol_error(code, body, expected_code, expected_type="BridgeProtocolError"):
    assert code != 0
    assert body["ok"] is False
    assert body["error"]["code"] == expected_code
    assert body["error"]["type"] == expected_type
    assert isinstance(body["error"]["message"], str)
    assert body["error"]["message"]


def main() -> int:
    snapshot = mathematics_case()
    original_snapshot = deepcopy(snapshot)
    exchange = {
        "version": "1.0",
        "student_ref": {"external_id": "fictional-bridge-001"},
        "learning_snapshot": snapshot,
        "request": {
            "subject": "mathematics",
            "intent": "continue",
            "duration_minutes": 30,
        },
    }

    code, body = call(envelope("plan", exchange, seed=91))
    assert code == 0, body
    assert body["ok"] is True
    assert body["result"]["student_ref"] == exchange["student_ref"]
    plan = body["result"]["plan"]
    assert plan["status"] == "ok"
    assert plan["session"]["duration_minutes"] == 30

    repeated_code, repeated_body = call(envelope("plan", exchange, seed=91))
    assert repeated_code == 0, repeated_body
    assert repeated_body["result"]["plan"]["session"] == plan["session"], (
        "bridge plan must preserve TutorLab determinism"
    )
    assert snapshot == original_snapshot, "bridge planning mutated the caller snapshot"

    planned_snapshot = with_objective_stack(snapshot, "mathematics", plan["objective_stack"])
    session = plan["session"]
    transition_exchange = {
        "version": "1.0",
        "student_ref": exchange["student_ref"],
        "learning_snapshot": planned_snapshot,
        "session_result": _all_correct_result(session),
        "metadata": {
            "subject": "mathematics",
            "session": session,
        },
    }
    transition_code, transition_body = call(envelope("transition", transition_exchange))
    assert transition_code == 0, transition_body
    assert transition_body["ok"] is True
    assert transition_body["result"]["student_ref"] == exchange["student_ref"]
    update = transition_body["result"]["transition"]
    assert update["evidence_events"]
    assert update["snapshot_update"]["recent_activity"]["session_ids"]
    assert update["next_step"]["action"] in {
        "recover",
        "consolidate",
        "advance",
        "extend",
        "reassess",
        "return_to",
    }

    wrong_subject = deepcopy(transition_exchange)
    wrong_subject["metadata"]["subject"] = "english"
    wrong_code, wrong_body = call(envelope("transition", wrong_subject))
    _assert_protocol_error(
        wrong_code,
        wrong_body,
        "TUTORLAB_VALIDATION_ERROR",
        expected_type="ValueError",
    )

    wrong_session = deepcopy(transition_exchange)
    wrong_session["session_result"]["session_id"] = "another-session"
    wrong_session_code, wrong_session_body = call(envelope("transition", wrong_session))
    _assert_protocol_error(
        wrong_session_code,
        wrong_session_body,
        "TUTORLAB_VALIDATION_ERROR",
        expected_type="ValueError",
    )

    missing_response = deepcopy(transition_exchange)
    del missing_response["session_result"]["responses"][0]["response"]
    missing_response_code, missing_response_body = call(envelope("transition", missing_response))
    _assert_protocol_error(
        missing_response_code,
        missing_response_body,
        "TUTORLAB_VALIDATION_ERROR",
        expected_type="ValueError",
    )

    bad_code, bad_body = call(envelope("unknown", {}))
    _assert_protocol_error(bad_code, bad_body, "UNSUPPORTED_OPERATION")

    missing_payload_code, missing_payload_body = call(
        {"bridge_version": BRIDGE_VERSION, "operation": "plan"}
    )
    _assert_protocol_error(missing_payload_code, missing_payload_body, "INVALID_PAYLOAD")

    bad_seed_code, bad_seed_body = call(envelope("plan", exchange, seed=True))
    _assert_protocol_error(bad_seed_code, bad_seed_body, "INVALID_SEED")

    wrong_version_code, wrong_version_body = call(
        {"bridge_version": "2.0", "operation": "plan", "payload": exchange}
    )
    _assert_protocol_error(
        wrong_version_code,
        wrong_version_body,
        "UNSUPPORTED_BRIDGE_VERSION",
    )

    extra_field_code, extra_field_body = call(envelope("plan", exchange, unexpected=True))
    _assert_protocol_error(extra_field_code, extra_field_body, "INVALID_ENVELOPE")

    transition_seed_code, transition_seed_body = call(
        envelope("transition", transition_exchange, seed=1)
    )
    _assert_protocol_error(transition_seed_code, transition_seed_body, "INVALID_ENVELOPE")

    invalid_exchange = deepcopy(exchange)
    invalid_exchange["version"] = "2.0"
    invalid_exchange_code, invalid_exchange_body = call(envelope("plan", invalid_exchange))
    _assert_protocol_error(
        invalid_exchange_code,
        invalid_exchange_body,
        "TUTORLAB_VALIDATION_ERROR",
        expected_type="ValueError",
    )

    non_object_code, non_object_body = call_raw("[]")
    _assert_protocol_error(non_object_code, non_object_body, "INVALID_ENVELOPE")

    invalid_json_code, invalid_json_body = call_raw("{not-json")
    _assert_protocol_error(invalid_json_code, invalid_json_body, "INVALID_JSON")

    empty_code, empty_body = call_raw("")
    _assert_protocol_error(empty_code, empty_body, "EMPTY_REQUEST")

    print("Tutor service JSON bridge v1.1: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
