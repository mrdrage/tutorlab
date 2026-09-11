import hashlib
import json

from engine.families_english import present_simple_task
from engine.families_english_year1_grammar_core import GRAMMAR_CORE_BUILDERS
from engine.families_english_year1_grammar_use import GRAMMAR_USE_BUILDERS
from engine.families_english_year1_lexis import LEXIS_BUILDERS
from engine.families_english_year1_productive import PRODUCTIVE_BUILDERS
from engine.families_english_year1_receptive import RECEPTIVE_BUILDERS
from engine.families_math import fraction_equivalence_task
from engine.families_math_year1_geometry import GEOMETRY_DATA_BUILDERS
from engine.families_math_year1_numbers import NUMBER_BUILDERS
from engine.families_math_year1_practices import PRACTICE_BUILDERS

REGISTRY = {
    "math.numbers.fraction-equivalence": fraction_equivalence_task,
    "eng.grammar.present_simple": present_simple_task,
}
for group in (
    NUMBER_BUILDERS,
    GEOMETRY_DATA_BUILDERS,
    PRACTICE_BUILDERS,
    GRAMMAR_CORE_BUILDERS,
    GRAMMAR_USE_BUILDERS,
    LEXIS_BUILDERS,
    RECEPTIVE_BUILDERS,
    PRODUCTIVE_BUILDERS,
):
    REGISTRY.update(group)


def fingerprint(family_id, params, phase=None):
    payload={"family_id":family_id,"params":params}
    if phase is not None:
        payload["phase"]=phase
    encoded=json.dumps(payload,sort_keys=True,ensure_ascii=False,separators=(",",":"))
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()[:20]


def supported_competencies():
    return set(REGISTRY)


def can_generate(competency_id):
    return competency_id in REGISTRY


def _builder(competency_id):
    if competency_id in REGISTRY: return REGISTRY[competency_id]
    raise ValueError(f"no task family registry for {competency_id}")


def build_unique_task(competency_id,phase,seed,band,support,task_id,history,max_attempts=12):
    builder=_builder(competency_id)
    history=set(history)
    last=None
    for attempt in range(max_attempts):
        item=builder(phase,seed+attempt*7919,band,support,task_id)
        fp=fingerprint(item["family_id"],item.get("generation_parameters",{}),phase)
        item["fingerprint"]=fp
        item["competency_id"]=competency_id
        last=item
        if fp not in history: return item
    last["generation_warning"]="history_exhausted"
    return last
