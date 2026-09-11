#!/usr/bin/env python3
import json
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))

from engine.learning_snapshot import competency_state, with_objective_stack
from engine.objective_stack import start_objective, push_recovery
from engine.path_selector import select_target, suggested_successor
from engine.plan_kernel import resolve
from engine.result_transition import transition
from engine.session_dispatch import dispatch
from engine.stack_bridge import ensure_stack
from examples.learning_snapshot.synthetic_cases import mathematics_case, english_case

POLICY=json.loads((ROOT/"config/adaptive-policy.json").read_text(encoding="utf-8"))


def answers(session):
    rows=[]
    for phase in session["phases"]:
        for task in phase.get("tasks",[]):
            row={"task_id":task["task_id"],"response":"fixture","status":"correct","score":1.0,"support_used":task["support_level"]}
            if phase["kind"] in {"transfer","transfer_probe","challenge"}: row["transfer_success"]=0.9
            rows.append(row)
    return rows


def build(snapshot,subject,target,seed):
    selection=select_target(snapshot,subject,target)
    stack=ensure_stack(snapshot["subjects"][subject].get("objective_stack"),selection,int(POLICY["max_recovery_depth"]))
    current=stack["frames"][-1]["competency_id"]
    plan=resolve(selection,stack,competency_state(snapshot,subject,current),suggested_successor(snapshot,subject,current),POLICY)
    if plan["kind"]!="session": return plan,None
    sent=dispatch(plan["target"],plan["action"],stack["root_target_id"],seed=seed,history_fingerprints=snapshot["recent_activity"]["fingerprints"])
    return plan,sent


def main():
    errors=[]
    math=mathematics_case(); plan,sent=build(math,"mathematics","math.numbers.fraction-equivalence",31)
    if plan.get("action")!="consolidate" or sent["status"]!="ok": errors.append("math plan should consolidate supported target")
    session=sent["session"]
    math=with_objective_stack(math,"mathematics",plan["stack"])
    result={"version":"0.1","session_id":session["session_id"],"completed_at":"2026-09-11T19:10:00+02:00","completion_status":"completed","responses":answers(session)}
    moved=transition(math,"mathematics",session,result,POLICY)
    updated=moved["snapshot_update"]
    if not updated["subjects"]["mathematics"]["evidence_events"]: errors.append("results did not become evidence")
    if session["session_id"] not in updated["recent_activity"]["session_ids"]: errors.append("session history missing")
    if not updated["recent_activity"]["fingerprints"]: errors.append("fingerprint history missing")

    repeated=dispatch("math.numbers.fraction-equivalence","consolidate","math.numbers.fraction-equivalence",seed=31,history_fingerprints=updated["recent_activity"]["fingerprints"])
    old=set(updated["recent_activity"]["fingerprints"])
    new=[task["fingerprint"] for phase in repeated["session"]["phases"] for task in phase.get("tasks",[])]
    if any(fp in old for fp in new): errors.append("history did not force fresh task fingerprints")

    unsupported=dispatch("math.numbers.signed-number-sense","reassess","math.numbers.signed-number-sense",seed=4)
    if unsupported["status"]!="needs_review": errors.append("generation capability boundary missing")

    eng=english_case(); eplan,esent=build(eng,"english","eng.grammar.present_simple",44)
    if eplan.get("action")!="consolidate" or esent["status"]!="ok": errors.append("english plan should consolidate supported target")

    stack=start_objective("math.numbers.fraction-equivalence")
    stack=push_recovery(stack,"math.numbers.fraction-meaning",reason="fixture",max_depth=2)
    recovery=resolve({"root_target_id":"math.numbers.fraction-equivalence","working_target_id":"math.numbers.fraction-meaning","reason":"fixture"},stack,competency_state(mathematics_case(),"mathematics","math.numbers.fraction-meaning"),"math.numbers.fraction-equivalence",POLICY)
    if recovery["kind"]!="return_to" or recovery["target"]!="math.numbers.fraction-equivalence": errors.append("secure recovery did not return to suspended target")

    resume=english_case(); resume["subjects"]["english"]["objective_stack"]=start_objective("eng.grammar.present_simple")
    if select_target(resume,"english")["reason"]!="resume_objective_stack": errors.append("active objective stack not resumed")

    if errors:
        print("Learning snapshot validation: FAILED")
        for error in errors: print("-",error)
        return 1
    print("Learning snapshot validation: OK")
    print("Math next step:",moved["next_step"])
    print("English action:",eplan["action"])
    return 0


if __name__=="__main__":
    raise SystemExit(main())
