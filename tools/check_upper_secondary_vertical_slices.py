#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))

from engine.curriculum_access import load_competency
from engine.learning_snapshot import competency_state,with_objective_stack
from engine.path_selector import select_target,suggested_successor
from engine.plan_kernel import resolve
from engine.result_transition import transition
from engine.session_dispatch import dispatch
from engine.stack_bridge import ensure_stack
from examples.learning_snapshot.synthetic_cases import state

POLICY=json.loads((ROOT/"config"/"adaptive-policy.json").read_text(encoding="utf-8"))


def ancestors(target):
    found=set(); stack=[target]
    while stack:
        cid=stack.pop()
        try: node=load_competency(cid)
        except Exception: continue
        for prereq in node.get("prerequisites",[]):
            if prereq not in found:
                found.add(prereq); stack.append(prereq)
    return found


def snapshot(subject,target,context):
    states={}
    for cid in ancestors(target):
        states[cid]=state(cid,"secure",0.88,0.92,0.86,0.84,0.80)
    states[target]=state(target,"developing",0.78,0.72,0.66,0.62,0.48)
    return {
        "version":"0.2",
        "academic_context":context,
        "subjects":{subject:{"typical_year":context["stage_year"],"competency_states":states,"evidence_events":[],"objective_stack":None,"last_recommendation":None}},
        "recent_activity":{"session_ids":[],"fingerprints":[]},
        "preferences":{"default_duration_minutes":45,"max_challenge_band":5},
    }


def answers(session):
    rows=[]
    for phase in session["phases"]:
        for task in phase.get("tasks",[]):
            row={"task_id":task["task_id"],"response":"synthetic tutor-scored response","status":"correct","score":1.0,"support_used":task["support_level"]}
            if phase["kind"] in {"transfer","transfer_probe","challenge"}: row["transfer_success"]=0.9
            rows.append(row)
    return rows


def run_case(subject,target,context,seed):
    data=snapshot(subject,target,context)
    selection=select_target(data,subject,target)
    if selection.get("working_target_id")!=target:
        return [f"{target}: prerequisite gating unexpectedly selected {selection}"],None
    stack=ensure_stack(None,selection,int(POLICY["max_recovery_depth"]))
    plan=resolve(selection,stack,competency_state(data,subject,target),suggested_successor(data,subject,target),POLICY)
    if plan.get("kind")!="session": return [f"{target}: expected session plan, got {plan}"],None
    sent=dispatch(plan["target"],plan["action"],stack["root_target_id"],seed=seed)
    if sent.get("status")!="ok": return [f"{target}: dispatch failed {sent}"],None
    session=sent["session"]
    data=with_objective_stack(data,subject,plan["stack"])
    result={"version":"0.1","session_id":session["session_id"],"completed_at":"2026-09-14T12:00:00+02:00","completion_status":"completed","responses":answers(session)}
    moved=transition(data,subject,session,result,POLICY)
    errors=[]
    update=moved["snapshot_update"]
    if not moved["evidence_events"]: errors.append(f"{target}: no evidence events produced")
    if session["session_id"] not in update["recent_activity"]["session_ids"]: errors.append(f"{target}: session history missing")
    if not update["recent_activity"]["fingerprints"]: errors.append(f"{target}: fingerprint history missing")
    if target not in update["subjects"][subject]["competency_states"]: errors.append(f"{target}: competency state disappeared")
    if moved["next_step"].get("action") not in {"recover","consolidate","advance","extend","reassess","return_to"}: errors.append(f"{target}: invalid next step {moved['next_step']}")
    return errors,moved


def main():
    errors=[]
    math_context={"school_stage":"upper_secondary","stage_year":5,"school_year":"2026/27","pathway_profile_id":"it.upper.liceo-scientifico","pathway_variant":"standard","curriculum_profile_ids":[]}
    eng_context={"school_stage":"upper_secondary","stage_year":5,"school_year":"2026/27","pathway_profile_id":"it.upper.liceo-scientifico","pathway_variant":"standard","curriculum_profile_ids":[]}
    math_target="math.us.scientifico.calculus.optimization"
    eng_target="eng.us.liceo.integrated.b2-target"
    for subject,target,context,seed in (("mathematics",math_target,math_context,91),("english",eng_target,eng_context,117)):
        case_errors,moved=run_case(subject,target,context,seed)
        errors.extend(case_errors)
        if moved and moved.get("pending_task_ids"):
            errors.append(f"{target}: tutor-scored fixture unexpectedly left pending tasks")
    if errors:
        print("Upper Secondary vertical slices: FAILED")
        for error in errors: print("-",error)
        return 1
    print("Upper Secondary vertical slices: OK")
    print("Math target:",math_target)
    print("English target:",eng_target)
    return 0

if __name__=="__main__": raise SystemExit(main())
