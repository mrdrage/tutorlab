import hashlib
import json

from engine.families_english import present_simple_task
from engine.families_math import fraction_equivalence_task


def fingerprint(family_id, params):
    payload=json.dumps({"family_id":family_id,"params":params},sort_keys=True,ensure_ascii=False,separators=(",",":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:20]


def _builder(competency_id):
    if competency_id=="math.numbers.fraction-equivalence": return fraction_equivalence_task
    if competency_id=="eng.grammar.present_simple": return present_simple_task
    raise ValueError(f"no task family registry for {competency_id}")


def build_unique_task(competency_id,phase,seed,band,support,task_id,history,max_attempts=12):
    builder=_builder(competency_id)
    history=set(history)
    last=None
    for attempt in range(max_attempts):
        item=builder(phase,seed+attempt*7919,band,support,task_id)
        fp=fingerprint(item["family_id"],item.get("generation_parameters",{}))
        item["fingerprint"]=fp
        item["competency_id"]=competency_id
        last=item
        if fp not in history: return item
    last["generation_warning"]="history_exhausted"
    return last
