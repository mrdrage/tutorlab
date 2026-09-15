#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SCHEMAS=ROOT/"schemas"


def main() -> int:
    request=json.loads((SCHEMAS/"tutor-request.schema.json").read_text(encoding="utf-8"))
    exchange=json.loads((SCHEMAS/"hub-exchange.schema.json").read_text(encoding="utf-8"))

    try:
        from jsonschema import Draft202012Validator, RefResolver
    except ImportError:
        print("jsonschema not installed: syntax-only contract check")
        assert request["type"]=="object" and exchange["type"]=="object"
        return 0

    Draft202012Validator.check_schema(request)
    Draft202012Validator.check_schema(exchange)

    request_validator=Draft202012Validator(request)
    request_validator.validate({"subject":"mathematics","intent":"continue","duration_minutes":40})
    request_validator.validate({"subject":"english","intent":"assessment","target_competency_id":"eng.grammar.present_simple"})

    invalid_cases=(
        {"subject":"physics","intent":"continue"},
        {"subject":"mathematics","intent":"magic"},
        {"subject":"mathematics","intent":"lesson","duration_minutes":5},
        {"subject":"mathematics","intent":"lesson","max_challenge_band":8},
    )
    for item in invalid_cases:
        assert list(request_validator.iter_errors(item)), item

    store={request["$id"]:request}
    resolver=RefResolver.from_schema(exchange,store=store)
    exchange_validator=Draft202012Validator(exchange,resolver=resolver)
    exchange_validator.validate({
        "version":"1.0",
        "student_ref":{"external_id":"fictional-001"},
        "learning_snapshot":{},
        "request":{"subject":"mathematics","intent":"continue"},
    })
    assert list(exchange_validator.iter_errors({
        "version":"2.0",
        "student_ref":{"external_id":"fictional-001"},
        "learning_snapshot":{},
    }))

    print("Tutor/Hub contract schemas: OK")
    return 0


if __name__=="__main__":
    raise SystemExit(main())
