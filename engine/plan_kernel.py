from engine.decision_bridge import route
from engine.objective_stack import complete_current, current_objective, push_recovery


def resolve(selection, stack, state, successor, policy, recovery_state=None):
    target=current_objective(stack)
    choice=route(state,policy,target,successor,len(stack.get("frames",[]))-1)

    if len(stack.get("frames",[]))>1 and choice.action in {"advance","extend"}:
        stack=complete_current(stack)
        resumed=current_objective(stack)
        return {
            "kind":"return_to",
            "target":resumed,
            "next_action":"reassess" if policy.get("post_recovery_reassess",True) else None,
            "stack":stack,
            "decision":choice,
        }

    if choice.action=="recover" and choice.recovery_competency_id:
        stack=push_recovery(stack,choice.recovery_competency_id,reason=choice.rationale,max_depth=int(policy["max_recovery_depth"]))
        return {"kind":"session","target":choice.recovery_competency_id,"action":"recover","stack":stack,"decision":choice}

    if choice.action=="advance" and choice.next_competency_id and len(stack.get("frames",[]))==1:
        return {"kind":"advance","target":choice.next_competency_id,"action":"advance","stack":stack,"decision":choice}

    return {"kind":"session","target":target,"action":choice.action,"stack":stack,"decision":choice}
