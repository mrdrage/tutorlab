#!/usr/bin/env python3
import json
from pathlib import Path

from engine.adaptive_engine import decide
from engine.evidence_model import aggregate_competency_state
from engine.session_engine import build_session
from engine.session_evaluator import results_to_evidence

ROOT=Path(__file__).resolve().parents[2]
ADAPTIVE=json.loads((ROOT/"config/adaptive-policy.json").read_text(encoding="utf-8"))


def responses_for(session,error_code,related=None):
    rows=[]
    for phase in session["phases"]:
        for task in phase.get("tasks",[]):
            err={"code":error_code,"description":"synthetic demo observation","observer_confidence":0.92}
            if related: err["related_competency_id"]=related
            rows.append({"task_id":task["task_id"],"response":"demo","status":"partially_correct","score":0.5,"support_used":task["support_level"],"observed_errors":[err],"transfer_success":0.3 if phase["kind"] in {"transfer","transfer_probe"} else None})
    return rows


def run_math():
    session=build_session("math.numbers.fraction-equivalence","advance",seed=101,challenge_band=2)
    result={"version":"0.1","session_id":session["session_id"],"completed_at":"2026-09-11T18:30:00+02:00","completion_status":"completed","responses":responses_for(session,"missing_prerequisite","math.numbers.fraction-meaning")}
    ev=results_to_evidence(session,result)["events"]
    state=aggregate_competency_state(session["target_competency_id"],ev,ADAPTIVE)
    decision=decide(state,ADAPTIVE,current_target_id=session["target_competency_id"],suggested_next_id="math.numbers.fraction-comparison")
    return {"session":session,"result":result,"state":state,"decision":decision.__dict__}


def run_english():
    session=build_session("eng.grammar.present_simple","consolidate",seed=202,challenge_band=2)
    result={"version":"0.1","session_id":session["session_id"],"completed_at":"2026-09-11T18:45:00+02:00","completion_status":"completed","responses":responses_for(session,"procedure_error")}
    ev=results_to_evidence(session,result)["events"]
    state=aggregate_competency_state(session["target_competency_id"],ev,ADAPTIVE)
    decision=decide(state,ADAPTIVE,current_target_id=session["target_competency_id"],suggested_next_id="eng.grammar.basic_questions")
    return {"session":session,"result":result,"state":state,"decision":decision.__dict__}


if __name__=="__main__":
    print(json.dumps({"mathematics":run_math(),"english":run_english()},ensure_ascii=False,indent=2))
