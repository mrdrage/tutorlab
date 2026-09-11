from __future__ import annotations


def _task_index(session):
    index={}
    for phase in session.get("phases",[]):
        for task in phase.get("tasks",[]):
            index[task["task_id"]]=(phase,task)
    return index


def auto_score(task,response):
    if task.get("response_mode") not in {"single_choice","short_answer"}: return None
    answer=task.get("solution",{}).get("answer")
    if answer is None: return None
    ok=str(response).strip().casefold()==str(answer).strip().casefold()
    return {"score":1.0 if ok else 0.0,"status":"correct" if ok else "incorrect"}


def results_to_evidence(session,result):
    tasks=_task_index(session); events=[]; pending=[]
    for number,item in enumerate(result.get("responses",[]),1):
        task_id=item.get("task_id")
        if task_id not in tasks: continue
        phase,task=tasks[task_id]
        status=item.get("status")
        score=item.get("score")
        if status=="needs_external_scoring" and score is None:
            pending.append(task_id); continue
        if status is None:
            auto=auto_score(task,item.get("response"))
            if auto is None: pending.append(task_id); continue
            status=auto["status"]; score=auto["score"]
        outcome={"status":status}
        if item.get("explanation_quality") is not None: outcome["explanation_quality"]=item["explanation_quality"]
        if item.get("transfer_success") is not None: outcome["transfer_success"]=item["transfer_success"]
        event={
            "event_id":f"{session['session_id']}-{task_id}-{number}",
            "competency_id":task.get("competency_id",session["target_competency_id"]),
            "observed_at":result["completed_at"],
            "task":{"task_id":task_id,"mode":phase["kind"],"context_familiarity":"near_transfer" if phase["kind"] in {"transfer","transfer_probe","challenge"} else "routine"},
            "outcome":outcome,
            "support":{"level":item.get("support_used","none")},
            "error_observations":item.get("observed_errors",[]),
            "tags":list(item.get("tags",[]))+[f"phase:{phase['kind']}"]
        }
        if score is not None: event["outcome"]["score"]=score
        events.append(event)
    return {"events":events,"pending_task_ids":pending}
