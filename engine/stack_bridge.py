from copy import deepcopy

from engine.objective_stack import start_objective, push_recovery


def ensure_stack(existing, selection, max_depth):
    if existing and existing.get("frames") and selection.get("reason") == "resume_objective_stack":
        return deepcopy(existing)
    stack=start_objective(selection["root_target_id"])
    if selection["working_target_id"]!=selection["root_target_id"]:
        stack=push_recovery(stack,selection["working_target_id"],reason=selection["reason"],max_depth=max_depth)
    return stack
