from engine.decision_bridge import route
from engine.learning_snapshot import apply_evidence, competency_state, with_objective_stack, with_recent_activity
from engine.objective_stack import complete_current, current_objective, push_recovery, start_objective
from engine.path_selector import suggested_successor
from engine.session_evaluator import results_to_evidence


def transition(data,subject,session,result,policy):
    converted=results_to_evidence(session,result)
    updated=apply_evidence(data,subject,converted["events"],policy)
    updated=with_recent_activity(updated,session)
    stack=updated["subjects"][subject].get("objective_stack") or start_objective(session["original_target_id"])
    target=session["target_competency_id"]
    choice=route(competency_state(updated,subject,target),policy,target,suggested_successor(updated,subject,target),len(stack.get("frames",[]))-1)

    if len(stack.get("frames",[]))>1 and current_objective(stack)==target and choice.action in {"advance","extend"}:
        stack=complete_current(stack); next_step={"action":"return_to","target":current_objective(stack),"reason":"recovery_secure"}
    elif choice.action=="recover" and choice.recovery_competency_id:
        try:
            stack=push_recovery(stack,choice.recovery_competency_id,reason=choice.rationale,max_depth=int(policy["max_recovery_depth"]))
            next_step={"action":"recover","target":choice.recovery_competency_id,"reason":choice.rationale}
        except ValueError:
            next_step={"action":"reassess","target":target,"reason":"maximum_recovery_depth_reached"}
    elif choice.action=="advance" and choice.next_competency_id:
        stack=start_objective(choice.next_competency_id); next_step={"action":"advance","target":choice.next_competency_id,"reason":choice.rationale}
    else:
        next_step={"action":choice.action,"target":target,"reason":choice.rationale}

    updated=with_objective_stack(updated,subject,stack)
    updated["subjects"][subject]["last_recommendation"]=next_step
    return {"snapshot_update":updated,"next_step":next_step,"pending_task_ids":converted["pending_task_ids"],"evidence_events":converted["events"]}
