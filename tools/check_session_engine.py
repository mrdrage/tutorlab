#!/usr/bin/env python3
import json
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))

from engine.session_engine import build_session,load_policy,student_view
from engine.session_evaluator import results_to_evidence
from engine.session_quality import validate_session


def fps(session):
    return {t["fingerprint"] for p in session["phases"] for t in p.get("tasks",[])}


def main():
    policy=load_policy(); errors=[]
    math=build_session("math.numbers.fraction-equivalence","advance",seed=17,challenge_band=2)
    eng=build_session("eng.grammar.present_simple","consolidate",seed=29,challenge_band=2)
    reassess=build_session("math.numbers.fraction-equivalence","reassess",seed=31)
    for name,session in (("math",math),("english",eng),("reassess",reassess)):
        for err in validate_session(session,policy): errors.append(f"{name}: {err}")

    if any("solution" in t for p in student_view(math)["phases"] for t in p.get("tasks",[])):
        errors.append("student view leaks solutions")

    repeated=build_session("math.numbers.fraction-equivalence","advance",seed=17,challenge_band=2,history_fingerprints=list(fps(math)))
    if fps(math) & fps(repeated): errors.append("anti-repetition failed for math demo")

    responses=[]
    open_ids=[]
    for p in math["phases"]:
        for t in p.get("tasks",[]):
            if t["response_mode"]=="open_response":
                responses.append({"task_id":t["task_id"],"response":"student text","status":"needs_external_scoring","support_used":"none"}); open_ids.append(t["task_id"])
            else:
                responses.append({"task_id":t["task_id"],"response":"demo","status":"correct","score":1.0,"support_used":t["support_level"]})
    result={"version":"0.1","session_id":math["session_id"],"completed_at":"2026-09-11T18:00:00+02:00","completion_status":"completed","responses":responses}
    converted=results_to_evidence(math,result)
    if set(converted["pending_task_ids"])!=set(open_ids): errors.append("open-response pending scoring mismatch")
    if len(converted["events"])!=len(responses)-len(open_ids): errors.append("evidence event count mismatch")
    if not all(e["competency_id"]=="math.numbers.fraction-equivalence" for e in converted["events"]): errors.append("wrong competency in evidence")

    if errors:
        print("Session engine validation: FAILED")
        for error in errors: print("-",error)
        return 1
    print("Session engine validation: OK")
    print("Math tasks:",len(fps(math)),"English tasks:",len(fps(eng)))
    return 0

if __name__=="__main__": raise SystemExit(main())
