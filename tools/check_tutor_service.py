#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone

from engine.tutor_service import hub_plan, hub_transition, persist_planned_stack, plan
from examples.learning_snapshot.synthetic_cases import mathematics_case


def _task_count(session):
    return sum(len(phase.get("tasks", [])) for phase in session.get("phases", []))


def _assert_student_safe(session):
    for phase in session.get("phases", []):
        for task in phase.get("tasks", []):
            for forbidden in ("solution", "rubric", "error_signals", "generation_parameters"):
                assert forbidden not in task, (task.get("task_id"), forbidden)


def _all_correct_result(session):
    responses=[]
    for phase in session.get("phases", []):
        for task in phase.get("tasks", []):
            responses.append({
                "task_id": task["task_id"],
                "status": "correct",
                "score": 1.0,
                "support_used": "none",
                "transfer_success": 1.0 if phase["kind"] in {"transfer", "transfer_probe", "challenge"} else None,
                "explanation_quality": 0.9 if phase["kind"] == "explanation" else None,
            })
    return {
        "completed_at": datetime.now(timezone.utc).isoformat(),
        "responses": responses,
    }


def _must_fail(fn, message):
    try:
        fn()
    except (ValueError, KeyError):
        return
    raise AssertionError(message)


def main() -> int:
    snapshot=mathematics_case()
    original=deepcopy(snapshot)

    _must_fail(lambda: plan(snapshot,{"subject":"physics","intent":"continue"}),"unsupported subject accepted")
    _must_fail(lambda: plan(snapshot,{"subject":"mathematics","intent":"magic"}),"unsupported intent accepted")
    _must_fail(lambda: plan(snapshot,{"subject":"mathematics","intent":"continue","quantity_hint":31}),"invalid quantity accepted")

    continued=plan(snapshot,{"subject":"mathematics","intent":"continue","duration_minutes":40},seed=101)
    continued_again=plan(snapshot,{"subject":"mathematics","intent":"continue","duration_minutes":40},seed=101)
    assert continued["status"]=="ok"
    assert continued["session"]==continued_again["session"], "fixed snapshot/request/seed must be deterministic"
    assert continued["session"]["duration_minutes"]==40
    assert continued["student_session"] is not None
    _assert_student_safe(continued["student_session"])

    target=continued["selection"]["root_target_id"]
    practiced=plan(snapshot,{"subject":"mathematics","intent":"practice","target_competency_id":target},seed=102)
    assert practiced["status"]=="ok"
    assert practiced["decision"]["action"] in {"recover","reassess","consolidate"}

    quantity=plan(snapshot,{"subject":"mathematics","intent":"practice","target_competency_id":target,"quantity_hint":12},seed=107)
    assert quantity["status"]=="ok"
    generation=quantity["session"]["generation"]
    actual=_task_count(quantity["session"])
    assert generation["task_quantity_requested"]==12
    assert generation["task_quantity_actual"]==actual
    assert actual>=generation["task_quantity_structural_minimum"]
    assert actual<=12
    assert generation["task_quantity_shortfall"]==12-actual
    assert generation["task_quantity_satisfied"]==(actual>=12)
    fingerprints=[task["fingerprint"] for phase in quantity["session"]["phases"] for task in phase.get("tasks",[])]
    assert len(fingerprints)==len(set(fingerprints)), "quantity expansion introduced duplicate fingerprints"
    _assert_student_safe(quantity["student_session"])

    assessed=plan(snapshot,{"subject":"mathematics","intent":"assessment","target_competency_id":target},seed=103)
    assert assessed["status"]=="ok"
    assert assessed["decision"]["action"]=="reassess"

    gated_target="math.numbers.fraction-operations"
    gated_practice=plan(snapshot,{"subject":"mathematics","intent":"practice","target_competency_id":gated_target},seed=105)
    assert gated_practice["selection"]["root_target_id"]==gated_target
    assert gated_practice["selection"]["working_target_id"]=="math.numbers.fraction-equivalence"
    assert gated_practice["decision"]["action"]=="recover", "practice must not bypass a known prerequisite gap"

    gated_assessment=plan(snapshot,{"subject":"mathematics","intent":"assessment","target_competency_id":gated_target},seed=106)
    assert gated_assessment["selection"]["working_target_id"]=="math.numbers.fraction-equivalence"
    assert gated_assessment["decision"]["action"]=="reassess", "assessment must test the selected prerequisite rather than bypass it"

    exchange={
        "version":"1.0",
        "student_ref":{"external_id":"fictional-student-001","display_name":"Studente fittizio"},
        "learning_snapshot":snapshot,
        "request":{"subject":"mathematics","intent":"continue","duration_minutes":35},
    }
    hub=hub_plan(exchange,seed=104)
    assert hub["version"]=="1.0" and hub["plan"]["status"]=="ok"

    planned_snapshot=persist_planned_stack(snapshot,"mathematics",hub["plan"])
    session=hub["plan"]["session"]
    result=_all_correct_result(session)
    roundtrip={
        "version":"1.0",
        "student_ref":exchange["student_ref"],
        "learning_snapshot":planned_snapshot,
        "session_result":result,
        "metadata":{"subject":"mathematics","session":session},
    }
    transitioned=hub_transition(roundtrip)
    update=transitioned["transition"]
    assert update["evidence_events"]
    assert update["snapshot_update"]["recent_activity"]["session_ids"]
    assert update["next_step"]["action"] in {"recover","consolidate","advance","extend","reassess","return_to"}

    wrong_subject=deepcopy(roundtrip)
    wrong_subject["metadata"]["subject"]="english"
    _must_fail(lambda: hub_transition(wrong_subject),"cross-subject session transition accepted")

    missing_student=deepcopy(exchange)
    missing_student["student_ref"]={}
    _must_fail(lambda: hub_plan(missing_student),"missing external student id accepted")

    assert snapshot==original, "plan/hub_plan mutated the caller snapshot"

    print("Tutor service v1.0 checks: OK")
    return 0


if __name__=="__main__":
    raise SystemExit(main())
