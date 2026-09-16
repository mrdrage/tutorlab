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
    return completed.returncode, body


def call(request):
    return call_raw(json.dumps(request, ensure_ascii=False))


def _all_correct_result(session):
    responses = []
    for phase in session.get("phases", []):
        for task in phase.get("tasks", []):
            responses.append(
                {
                    "task_id": task["task_id"],
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
        "completed_at": datetime.now(timezone.utc).isoformat(),
        "responses": responses,
    }


def _assert_protocol_error(code, body, expected_type):
    assert code != 0
    assert body["ok"] is False
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

    code, body = call({"operation": "plan", "payload": exchange, "seed": 91})
    assert code == 0, body
    assert body["ok"] is True
    assert body["result"]["student_ref"] == exchange["student_ref"]
    plan = body["result"]["plan"]
    assert plan["status"] == "ok"
    assert plan["session"]["duration_minutes"] == 30

    repeated_code, repeated_body = call({"operation": "plan", "payload": exchange, "seed": 91})
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
    transition_code, transition_body = call(
        {"operation": "transition", "payload": transition_exchange}
    )
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
    wrong_code, wrong_body = call({"operation": "transition", "payload": wrong_subject})
    _assert_protocol_error(wrong_code, wrong_body, "ValueError")

    bad_code, bad_body = call({"operation": "unknown", "payload": {}})
    _assert_protocol_error(bad_code, bad_body, "ValueError")

    missing_payload_code, missing_payload_body = call({"operation": "plan"})
    _assert_protocol_error(missing_payload_code, missing_payload_body, "ValueError")

    bad_seed_code, bad_seed_body = call(
        {"operation": "plan", "payload": exchange, "seed": True}
    )
    _assert_protocol_error(bad_seed_code, bad_seed_body, "ValueError")

    non_object_code, non_object_body = call_raw("[]")
    _assert_protocol_error(non_object_code, non_object_body, "ValueError")

    invalid_json_code, invalid_json_body = call_raw("{not-json")
    _assert_protocol_error(invalid_json_code, invalid_json_body, "JSONDecodeError")

    empty_code, empty_body = call_raw("")
    _assert_protocol_error(empty_code, empty_body, "ValueError")

    print("Tutor service JSON bridge v1.1: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
