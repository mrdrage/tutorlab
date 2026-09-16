#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = ROOT / "schemas"


def _load(name: str):
    return json.loads((SCHEMAS / name).read_text(encoding="utf-8"))


def main() -> int:
    tutor_request = _load("tutor-request.schema.json")
    hub_exchange = _load("hub-exchange.schema.json")
    bridge_request = _load("tutor-service-bridge-request.schema.json")
    bridge_response = _load("tutor-service-bridge-response.schema.json")

    for schema in (tutor_request, hub_exchange, bridge_request, bridge_response):
        assert isinstance(schema, dict)
        assert schema.get("$schema") == "https://json-schema.org/draft/2020-12/schema"

    try:
        from jsonschema import Draft202012Validator, RefResolver
    except ImportError:
        print("jsonschema not installed: syntax-only JSON bridge schema check")
        return 0

    for schema in (tutor_request, hub_exchange, bridge_request, bridge_response):
        Draft202012Validator.check_schema(schema)

    store = {
        tutor_request["$id"]: tutor_request,
        hub_exchange["$id"]: hub_exchange,
        bridge_request["$id"]: bridge_request,
        bridge_response["$id"]: bridge_response,
    }
    request_resolver = RefResolver.from_schema(bridge_request, store=store)
    request_validator = Draft202012Validator(bridge_request, resolver=request_resolver)
    response_validator = Draft202012Validator(bridge_response)

    plan_payload = {
        "version": "1.0",
        "student_ref": {"external_id": "fictional-schema-001"},
        "learning_snapshot": {},
        "request": {"subject": "mathematics", "intent": "continue"},
    }
    request_validator.validate(
        {
            "bridge_version": "1.0",
            "operation": "plan",
            "payload": plan_payload,
            "seed": 7,
        }
    )

    transition_payload = {
        "version": "1.0",
        "student_ref": {"external_id": "fictional-schema-001"},
        "learning_snapshot": {},
        "session_result": {},
        "metadata": {
            "subject": "mathematics",
            "session": {},
        },
    }
    request_validator.validate(
        {
            "bridge_version": "1.0",
            "operation": "transition",
            "payload": transition_payload,
        }
    )

    invalid_requests = (
        {
            "operation": "plan",
            "payload": plan_payload,
        },
        {
            "bridge_version": "2.0",
            "operation": "plan",
            "payload": plan_payload,
        },
        {
            "bridge_version": "1.0",
            "operation": "plan",
            "payload": plan_payload,
            "seed": True,
        },
        {
            "bridge_version": "1.0",
            "operation": "transition",
            "payload": transition_payload,
            "seed": 1,
        },
        {
            "bridge_version": "1.0",
            "operation": "transition",
            "payload": {
                "version": "1.0",
                "student_ref": {"external_id": "fictional-schema-001"},
                "learning_snapshot": {},
                "session_result": {},
                "metadata": {"subject": "mathematics"},
            },
        },
    )
    for item in invalid_requests:
        assert list(request_validator.iter_errors(item)), item

    response_validator.validate(
        {
            "bridge_version": "1.0",
            "ok": True,
            "result": {},
        }
    )
    response_validator.validate(
        {
            "bridge_version": "1.0",
            "ok": False,
            "error": {
                "code": "INVALID_JSON",
                "type": "BridgeProtocolError",
                "message": "bridge request is not valid JSON",
            },
        }
    )

    invalid_responses = (
        {"ok": True, "result": {}},
        {
            "bridge_version": "1.0",
            "ok": False,
            "error": {
                "code": "UNKNOWN_CODE",
                "type": "ValueError",
                "message": "bad",
            },
        },
        {
            "bridge_version": "1.0",
            "ok": True,
            "result": {},
            "error": {},
        },
    )
    for item in invalid_responses:
        assert list(response_validator.iter_errors(item)), item

    print("Tutor service JSON bridge schemas v1.1: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
