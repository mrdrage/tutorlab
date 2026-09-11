from engine.session_engine import build_session
from engine.task_families import can_generate

DEFAULT_BANDS={"recover":1,"consolidate":2,"advance":2,"extend":4,"reassess":2}


def dispatch(target,action,root_target,seed=1,duration_minutes=None,max_challenge_band=5,history_fingerprints=None):
    if not can_generate(target):
        return {"status":"needs_review","warning":f"task_family_not_available:{target}","session":None}
    session=build_session(
        target,
        action,
        original_target_id=root_target,
        challenge_band=min(DEFAULT_BANDS[action],int(max_challenge_band)),
        duration_minutes=duration_minutes,
        seed=seed,
        history_fingerprints=history_fingerprints or [],
    )
    return {"status":"ok","warning":None,"session":session}
