from __future__ import annotations

import random

from engine.families_upper_secondary import _index, _rubric
from engine.generation_common import open_task, phase_mode, task


def _grammar_builder(cid,cases):
    def build(phase,seed,band,support,task_id):
        node=_index("english")[cid]; mode=phase_mode(phase); rng=random.Random(seed)
        prompt,answer,meaning=rng.choice(cases); rubric=_rubric(node,node["title"])
        params={"competency":cid,"phase":phase,"seed":seed}
        errors=node.get("diagnostic_signals",[])
        if mode=="model":
            return open_task(task_id,"upper.eng.grammar.model",f"Worked example: {prompt} Model answer: {answer}. Explain how the form expresses {meaning}.",band,support,params=params,dimensions=["grammar_control","explanation","accuracy"],rubric=rubric,acceptable=f"links {answer} to {meaning}",errors=errors)
        if mode=="transfer":
            return open_task(task_id,"upper.eng.grammar.transfer",f"{prompt} Then write a different sentence that expresses {meaning} in a new context.",band,support,params=params,dimensions=["accuracy","transfer","grammar_control"],rubric=rubric,acceptable=answer,errors=errors)
        return task(task_id,"upper.eng.grammar.control",prompt,answer,band,support,params=params,dimensions=["accuracy","grammar_control"],rubric=rubric,errors=errors)
    return build


GRAMMAR_CASES={
"eng.us.grammar.tense-control-b1":[
    ("Complete: Yesterday I ___ (finish) the project before dinner.","finished","a completed past event"),
    ("Complete: This time tomorrow we ___ (travel) to Rome.","will be travelling","an action in progress at a future time"),
    ("Complete: She usually ___ (study) in the library after school.","studies","a present routine")
],
"eng.us.grammar.modals-b1":[
    ("Choose the best modal: You ___ wear a seat belt; it is required.","must","strong obligation"),
    ("Choose the best modal: You look tired. You ___ take a break.","should","advice"),
    ("Choose the best modal: It ___ rain later, so take an umbrella.","might","possibility")
],
"eng.us.grammar.aspect-b1":[
    ("Complete: I ___ (live) here for three years.","have lived","duration continuing to the present"),
    ("Complete: I ___ (visit) London in 2024.","visited","a finished event at a defined past time"),
    ("Complete: She ___ never ___ (try) sushi.","has never tried","life experience without a defined past time")
],
"eng.us.grammar.conditionals-b1":[
    ("Complete: If it rains tomorrow, we ___ (stay) at home.","will stay","a probable future consequence"),
    ("Complete: If I had more free time, I ___ (learn) another language.","would learn","a less real or hypothetical situation"),
    ("Complete: If you heat ice, it ___ (melt).","melts","a general result")
],
"eng.us.grammar.complex-sentences-b1plus":[
    ("Join with a relative clause: I met a student. The student speaks three languages.","I met a student who speaks three languages.","a relative clause linking information"),
    ("Join naturally: The course was difficult. I completed it successfully. Use although.","Although the course was difficult, I completed it successfully.","concession"),
    ("Join naturally: We left early. We wanted to avoid traffic. Use because or so that.","We left early because we wanted to avoid traffic.","reason or purpose")
],
"eng.us.liceo.grammar.b2-control":[
    ("Complete: If the team ___ (test) the idea earlier, it might have avoided the problem.","had tested","an unreal past condition"),
    ("Rewrite in the passive: People expect the project to finish in June.","The project is expected to finish in June.","impersonal reporting and passive control"),
    ("Complete: Hardly ___ we arrived when the meeting started.","had","inversion in a marked formal structure")
]
}

UPPER_ENGLISH_GRAMMAR_OVERRIDES={cid:_grammar_builder(cid,cases) for cid,cases in GRAMMAR_CASES.items()}
