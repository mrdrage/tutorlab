from engine.adaptive_engine import decide


def route(state, policy, target, successor=None, depth=0):
    return decide(state, policy, current_target_id=target, suggested_next_id=successor, recovery_depth=depth)
