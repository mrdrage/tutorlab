#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

try:
    from jsonschema import Draft202012Validator
except ImportError:
    Draft202012Validator = None

from engine.objective_stack import start_objective
from engine.tutor_orchestrator import complete_tutor_session, prepare_tutor_package
from examples.learning_snapshot.synthetic_cases import mathematics_case

SCHEMA_NAMES = (
    "tutor-request.schema.json",
    "tutor-package.schema.json",
    "tutor-transition.schema.json",
    "session-plan.schema.json",
)


def load_schema(name: str) -> dict:
    return json.loads((ROOT / "schemas" / name).read_text(encoding="utf-8"))


def result_for(session: dict) -> dict:
    responses = []
    for phase in session.get("phases", []):
        for task in phase.get("tasks", []):
            row = {
                "task_id": task["task_id"],
                "response": "schema fixture",
                "status": "correct",
                "score": 1.0,
                "support_used": task.get("support_level", "none"),
                "explanation_quality": 0.9,
            }
            if phase.get("kind") in {"transfer", "transfer_probe", "challenge"}:
                row["transfer_success"] = 0.9
            responses.append(row)
    return {
        "version": "0.1",
        "session_id": session["session_id"],
        "completed_at": "2026-09-14T16:15:00+02:00",
        "completion_status": "completed",
        "responses": responses,
    }


def language_snapshot() -> dict:
    target = "ita.grammar.orthography-punctuation"
    return {
        "version": "0.1",
        "subjects": {
            "italian": {
                "typical_year": 1,
                "competency_states": {},
                "evidence_events": [],
                "objective_stack": start_objective(target),
                "last_recommendation": None,
            }
        },
        "recent_activity": {"session_ids": [], "fingerprints": []},
        "preferences": {"default_duration_minutes": 35, "max_challenge_band": 4},
    }


def main() -> int:
    failures = []
    schemas = {name: load_schema(name) for name in SCHEMA_NAMES}

    if Draft202012Validator is None:
        print("Tutor contract schemas: jsonschema unavailable; JSON parsing only")
        return 0

    validators = {}
    for name, schema in schemas.items():
        try:
            Draft202012Validator.check_schema(schema)
            validators[name] = Draft202012Validator(schema)
        except Exception as exc:
            failures.append(f"{name}: invalid Draft 2020-12 schema: {exc}")

    valid_request = {
        "version": "1.0-rc1",
        "subject": "mathematics",
        "requested_target_id": "math.numbers.fraction-equivalence",
        "duration_minutes": 40,
        "seed": 77,
        "intent": "adaptive",
        "max_challenge_band": 4,
        "output": "both",
    }
    request_validator = validators.get("tutor-request.schema.json")
    if request_validator:
        if list(request_validator.iter_errors(valid_request)):
            failures.append("valid TutorRequest rejected")
        negative_requests = (
            {**valid_request, "subject": "physics"},
            {**valid_request, "duration_minutes": 5},
            {**valid_request, "intent": "cram"},
            {**valid_request, "unexpected": True},
            {**valid_request, "requested_target_id": ""},
        )
        for index, candidate in enumerate(negative_requests, 1):
            if not list(request_validator.iter_errors(candidate)):
                failures.append(f"invalid TutorRequest #{index} was accepted")

    package = prepare_tutor_package(mathematics_case(), valid_request)
    package_validator = validators.get("tutor-package.schema.json")
    if package_validator:
        errors = list(package_validator.iter_errors(package))
        if errors:
            failures.append(f"generated TutorPackage rejected: {errors[0].message}")

    session_validator = validators.get("session-plan.schema.json")
    if session_validator and package.get("session"):
        errors = list(session_validator.iter_errors(package["session"]))
        if errors:
            failures.append(f"generated mathematics session rejected: {errors[0].message}")

    if package.get("session"):
        transition = complete_tutor_session(mathematics_case(), package, result_for(package["session"]))
        transition_validator = validators.get("tutor-transition.schema.json")
        if transition_validator:
            errors = list(transition_validator.iter_errors(transition))
            if errors:
                failures.append(f"generated TutorTransition rejected: {errors[0].message}")

    italian_package = prepare_tutor_package(language_snapshot(), {
        "version": "1.0-rc1",
        "subject": "italian",
        "intent": "assessment",
        "output": "student",
        "seed": 78,
    })
    if session_validator and italian_package.get("session"):
        errors = list(session_validator.iter_errors(italian_package["session"]))
        if errors:
            failures.append(f"Italian session-plan contract is still out of sync: {errors[0].message}")

    if package_validator:
        broken = copy.deepcopy(package)
        broken["status"] = "maybe"
        if not list(package_validator.iter_errors(broken)):
            failures.append("TutorPackage accepted invalid status")

    if failures:
        print("Tutor contract schemas: FAILED")
        for failure in failures:
            print("-", failure)
        return 1

    print("Tutor contract schemas: OK")
    print("Draft 2020-12 schemas: 4")
    print("Generated TutorRequest/Package/Transition: valid")
    print("Italian session-plan schema alignment: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
