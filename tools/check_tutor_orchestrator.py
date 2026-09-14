#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from engine.objective_stack import start_objective
from engine.plan_kernel import resolve
from engine.tutor_orchestrator import complete_tutor_session, prepare_tutor_package
from examples.learning_snapshot.synthetic_cases import english_case, mathematics_case

POLICY = json.loads((ROOT / "config" / "adaptive-policy.json").read_text(encoding="utf-8"))
FORBIDDEN_STUDENT_KEYS = {"solution", "rubric", "error_signals", "generation_parameters", "history_fingerprints"}


def snapshot(subject: str, target: str, *, year: int = 1, upper_context: dict | None = None) -> dict:
    data = {
        "version": "0.2" if upper_context else "0.1",
        "subjects": {
            subject: {
                "typical_year": year,
                "competency_states": {},
                "evidence_events": [],
                "objective_stack": start_objective(target),
                "last_recommendation": None,
            }
        },
        "recent_activity": {"session_ids": [], "fingerprints": []},
        "preferences": {"default_duration_minutes": 40, "max_challenge_band": 4},
    }
    if upper_context:
        data["academic_context"] = upper_context
    return data


def scored_result(session: dict) -> dict:
    responses = []
    for phase in session.get("phases", []):
        for task in phase.get("tasks", []):
            row = {
                "task_id": task["task_id"],
                "response": "synthetic response",
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
        "completed_at": "2026-09-14T16:00:00+02:00",
        "completion_status": "completed",
        "responses": responses,
    }


def forbidden_keys(value) -> set[str]:
    found = set()
    if isinstance(value, dict):
        for key, child in value.items():
            if key in FORBIDDEN_STUDENT_KEYS:
                found.add(key)
            found.update(forbidden_keys(child))
    elif isinstance(value, list):
        for child in value:
            found.update(forbidden_keys(child))
    return found


def main() -> int:
    failures = []

    math = mathematics_case()
    package = prepare_tutor_package(math, {
        "version": "1.0-rc1",
        "subject": "mathematics",
        "requested_target_id": "math.numbers.fraction-equivalence",
        "duration_minutes": 40,
        "seed": 101,
        "intent": "adaptive",
        "output": "both",
    }, policy=POLICY)
    if package["status"] != "ok":
        failures.append("adaptive mathematics request did not produce a session")
    if package["session"] and package["session"]["duration_minutes"] != 40:
        failures.append("explicit duration was not respected")
    if package["plan"]["action"] != "consolidate":
        failures.append(f"expected fraction-equivalence consolidation, got {package['plan']}")
    if not package["views"]["tutor"] or not package["views"]["student"]:
        failures.append("both output did not produce tutor and student views")
    leaks = forbidden_keys(package["views"]["student"])
    if leaks:
        failures.append(f"student view leaked tutor-only keys: {sorted(leaks)}")

    if package.get("session"):
        completed = complete_tutor_session(math, package, scored_result(package["session"]), policy=POLICY)
        if not completed["evidence_events"]:
            failures.append("complete() did not produce evidence events")
        if completed["pending_task_ids"]:
            failures.append("explicitly scored responses unexpectedly remained pending")
        updated = completed["snapshot_update"]
        if package["session"]["session_id"] not in updated["recent_activity"]["session_ids"]:
            failures.append("complete() did not update session history")
        if completed["next_step"]["action"] not in {"recover", "consolidate", "advance", "extend", "reassess", "return_to"}:
            failures.append(f"invalid next step from complete(): {completed['next_step']}")

    eng = english_case()
    practice = prepare_tutor_package(eng, {
        "version": "1.0-rc1",
        "subject": "english",
        "requested_target_id": "eng.grammar.present_simple",
        "intent": "practice",
        "output": "student",
        "seed": 102,
    }, policy=POLICY)
    if practice["plan"]["action"] != "consolidate":
        failures.append("practice intent must create consolidation on the routed working target")
    if practice["views"]["tutor"] is not None or practice["views"]["student"] is None:
        failures.append("student-only output mode not respected")

    language_targets = {
        "italian": "ita.grammar.orthography-punctuation",
        "french": "fr.grammar.identity-possession",
        "spanish": "es.grammar.identity-possession",
    }
    for offset, (subject, target) in enumerate(language_targets.items(), 1):
        data = snapshot(subject, target)
        package_language = prepare_tutor_package(data, {
            "version": "1.0-rc1",
            "subject": subject,
            "intent": "assessment" if subject == "italian" else "diagnostic",
            "output": "both",
            "seed": 200 + offset,
        }, policy=POLICY)
        if package_language["status"] != "ok":
            failures.append(f"{subject}: orchestrator did not produce executable session")
        if package_language["plan"]["action"] != "reassess":
            failures.append(f"{subject}: assessment/diagnostic intent must use reassess")
        if package_language.get("session", {}).get("subject") != subject:
            failures.append(f"{subject}: session subject mismatch")

    upper = snapshot(
        "mathematics",
        "math.us.scientifico.calculus.optimization",
        year=5,
        upper_context={
            "school_stage": "upper_secondary",
            "stage_year": 5,
            "school_year": "2026/27",
            "pathway_profile_id": "it.upper.liceo-scientifico",
            "pathway_variant": "standard",
            "curriculum_profile_ids": [],
        },
    )
    upper_package = prepare_tutor_package(upper, {
        "version": "1.0-rc1",
        "subject": "mathematics",
        "intent": "practice",
        "duration_minutes": 55,
        "seed": 301,
    }, policy=POLICY)
    if upper_package["status"] != "ok":
        failures.append("upper-secondary target did not pass through tutor orchestrator")
    if upper_package.get("session", {}).get("target_competency_id") != "math.us.scientifico.calculus.optimization":
        failures.append("upper-secondary target changed unexpectedly")

    out_of_scope = snapshot("mathematics", "math.future.out-of-scope")
    review = prepare_tutor_package(out_of_scope, {
        "version": "1.0-rc1",
        "subject": "mathematics",
        "intent": "practice",
        "seed": 401,
    }, policy=POLICY)
    if review["status"] != "needs_review" or review["session"] is not None:
        failures.append("capability boundary not preserved by tutor orchestrator")

    strong_state = {
        "competency_id": "math.numbers.fraction-meaning",
        "status": "secure",
        "confidence": 0.92,
        "mastery": {"accuracy": 0.94, "independence": 0.90, "stability": 0.88, "transfer": 0.82},
        "evidence_summary": {"independent_event_count": 4, "transfer_event_count": 2, "contradiction_level": 0.0},
        "error_hypotheses": [],
    }
    advance = resolve(
        {"root_target_id": "math.numbers.fraction-meaning", "working_target_id": "math.numbers.fraction-meaning", "reason": "fixture"},
        start_objective("math.numbers.fraction-meaning"),
        strong_state,
        "math.numbers.fraction-equivalence",
        POLICY,
    )
    if advance.get("kind") != "advance":
        failures.append(f"strong state did not produce advance fixture: {advance.get('kind')}")
    elif advance["stack"]["root_target_id"] != "math.numbers.fraction-equivalence":
        failures.append("advance plan kept stale objective stack root")

    if failures:
        print("Tutor Orchestrator validation: FAILED")
        for failure in failures:
            print("-", failure)
        return 1

    print("Tutor Orchestrator validation: OK")
    print("Five subjects covered: mathematics, english, italian, french, spanish")
    print("Upper-secondary facade: OK")
    print("Student-view leakage guard: OK")
    print("Prepare -> complete transition: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
