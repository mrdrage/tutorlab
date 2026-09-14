from __future__ import annotations

import random

from engine.families_upper_secondary import _index, _rubric
from engine.generation_common import open_task, phase_mode

PROFESSIONAL_SCENARIOS=(
    "a short technical briefing before a task",
    "a customer request that contains one unclear requirement",
    "a project update with a delay and a proposed solution",
    "a simple procedure that must be explained to a new colleague",
)

INTERCULTURAL_SCENARIOS=(
    "different expectations about punctuality in formal and informal situations",
    "how direct or indirect a request can sound in different contexts",
    "different conventions for school or workplace communication",
    "how media can simplify cultural differences into stereotypes",
)


def _professional_builder(cid):
    def build(phase,seed,band,support,task_id):
        node=_index("english")[cid]; mode=phase_mode(phase); rng=random.Random(seed)
        scenario=rng.choice(PROFESSIONAL_SCENARIOS); rubric=_rubric(node,node["title"])
        if mode=="model":
            prompt=("Model: identify the key term, explain it in simpler English, use it in one realistic instruction, "
                    f"and check understanding. Apply this model to {scenario}.")
        else:
            prompt=(f"In {scenario}, use the target professional vocabulary accurately, paraphrase one technical term "
                    "for a non-specialist, and confirm one operational detail.")
        return open_task(task_id,f"upper.eng.professional.{mode}",prompt,band,support,
            params={"competency":cid,"phase":phase,"seed":seed,"scenario":scenario},
            dimensions=["vocabulary","register","paraphrase","task_completion"],
            rubric=rubric,acceptable="accurate professional meaning plus accessible paraphrase",
            errors=node.get("diagnostic_signals",[]))
    return build


def _intercultural_builder(cid):
    def build(phase,seed,band,support,task_id):
        node=_index("english")[cid]; mode=phase_mode(phase); rng=random.Random(seed)
        scenario=rng.choice(INTERCULTURAL_SCENARIOS); rubric=_rubric(node,node["title"])
        if mode=="model":
            prompt=("Model reasoning: describe the context, compare two plausible perspectives, support the comparison with evidence, "
                    f"and avoid absolute claims. Apply the structure to: {scenario}.")
        else:
            prompt=(f"Discuss {scenario}. Compare at least two context-sensitive perspectives, identify one possible stereotype, "
                    "and reformulate it in a more evidence-based way.")
        return open_task(task_id,f"upper.eng.intercultural.{mode}",prompt,band,support,
            params={"competency":cid,"phase":phase,"seed":seed,"scenario":scenario},
            dimensions=["intercultural","reasoning","language_demand","evidence_use"],
            rubric=rubric,acceptable="contextualised comparison without rigid generalisation",
            errors=node.get("diagnostic_signals",[]))
    return build


UPPER_ENGLISH_OVERRIDES={}
for cid,node in _index("english").items():
    if node.get("strand")=="professional_language": UPPER_ENGLISH_OVERRIDES[cid]=_professional_builder(cid)
    elif node.get("strand")=="intercultural": UPPER_ENGLISH_OVERRIDES[cid]=_intercultural_builder(cid)
