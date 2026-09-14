from __future__ import annotations

import json
import random
from functools import lru_cache
from pathlib import Path

from engine.generation_common import open_task, phase_mode, task

ROOT = Path(__file__).resolve().parents[1]


def _graphs(subject: str):
    base = ROOT / "curriculum" / "upper-secondary" / subject
    for path in sorted(base.rglob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        for node in data.get("nodes", []):
            yield node


@lru_cache(maxsize=None)
def _index(subject: str):
    result = {}
    for node in _graphs(subject):
        cid = node["id"]
        if cid in result:
            raise ValueError(f"duplicate upper-secondary competency id: {cid}")
        result[cid] = node
    return result


def _rubric(node, label: str):
    evidence = node.get("mastery_evidence", [])
    text = " ".join(evidence[:2]) if evidence else f"Dimostra {label} con ragionamento pertinente e comprensibile."
    return {"full_credit": text}


def _math_case(node, seed: int):
    rng = random.Random(seed)
    cid = node["id"]
    strand = node.get("strand", "mathematics")

    if "derivative" in cid or "derivat" in cid or "optimization" in cid:
        a = rng.choice([2, 3, 4])
        b = rng.choice([1, 2, 5])
        return (f"Per f(x)={a}x^2+{b}x, determina f'(x).", f"{2*a}x+{b}", "calculus")
    if "integral" in cid or "integr" in cid:
        a = rng.choice([2, 4, 6, 8])
        return (f"Calcola una primitiva di f(x)={a}x.", f"{a//2}x^2+C", "calculus")
    if "limit" in cid or "analysis" in cid:
        a = rng.choice([2, 3, 4, 5])
        return (f"Calcola lim x→{a} di (x^2-{a*a})/(x-{a}).", str(2*a), "calculus")
    if strand == "trigonometry" or "trigon" in cid:
        opposite, adjacent, hyp = rng.choice([(3, 4, 5), (5, 12, 13), (8, 15, 17)])
        return (f"In un triangolo rettangolo, rispetto all'angolo α il cateto opposto misura {opposite} e l'ipotenusa {hyp}. Calcola sin α.", f"{opposite}/{hyp}", "trigonometry")
    if strand in {"exponential_log", "exponential_logarithmic"} or "explog" in cid or "logarith" in cid:
        base = rng.choice([2, 3, 5, 10])
        exp = rng.choice([2, 3])
        value = base ** exp
        return (f"Risolvi {base}^x={value}.", str(exp), "exponential_log")
    if strand == "sequences" or "sequence" in cid:
        start = rng.choice([2, 3, 5, 7])
        step = rng.choice([2, 3, 4, 5])
        return (f"La successione inizia {start}, {start+step}, {start+2*step}. Qual è il termine successivo?", str(start+3*step), "sequences")
    if strand in {"statistics_probability", "data_probability"} or "probability" in cid or "statistic" in cid:
        values = rng.choice([[2, 4, 4, 6, 9], [3, 5, 5, 8, 12], [1, 2, 7, 7, 10]])
        return (f"Dati {values}, determina la mediana.", str(sorted(values)[2]), "statistics_probability")
    if strand in {"geometry", "analytic_geometry"} or "geometry" in cid or "vector" in cid:
        x, y, distance = rng.choice([(3, 4, 5), (5, 12, 13), (8, 15, 17)])
        return (f"Nel piano cartesiano A=(0,0) e B=({x},{y}). Calcola la distanza AB.", str(distance), "geometry")
    if strand == "functions" or "function" in cid:
        m = rng.choice([2, 3, -2, -3])
        q = rng.choice([1, 4, -1, 5])
        x = rng.choice([2, 3, 4])
        return (f"Per f(x)={m}x+({q}), calcola f({x}).", str(m*x+q), "functions")
    if strand in {"equations_inequalities", "algebra"} or "algebra" in cid or "equation" in cid or "inequal" in cid:
        if "quadratic" in cid:
            r1, r2 = rng.choice([(2, 3), (1, 4), (-2, 3)])
            b = -(r1 + r2)
            c = r1 * r2
            sign = "+" if b >= 0 else "-"
            return (f"Risolvi x^2 {sign} {abs(b)}x + ({c})=0.", f"x={r1} oppure x={r2}", "quadratic")
        if "inequal" in cid:
            limit = rng.choice([3, 4, 5])
            a = rng.choice([2, 3])
            b = rng.choice([1, 2])
            rhs = a * limit + b
            return (f"Risolvi {a}x+{b}<{rhs}.", f"x<{limit}", "inequality")
        solution = rng.choice([2, 4, 5, 7])
        a = rng.choice([2, 3, 4])
        b = rng.choice([1, 5, 7])
        rhs = a * solution + b
        return (f"Risolvi {a}x+{b}={rhs} e verifica la soluzione.", f"x={solution}", "algebra")
    scenario = rng.choice([
        "confrontare il costo di due tariffe",
        "scegliere un modello per una crescita nel tempo",
        "interpretare una tabella di misure sperimentali",
        "valutare la plausibilità di una previsione quantitativa",
    ])
    return (f"Devi {scenario}. Spiega quale rappresentazione o modello useresti e perché.", "valutazione tramite rubrica", "modelling")


def _math_builder(cid: str):
    def build(phase, seed, band, support, task_id):
        node = _index("mathematics")[cid]
        mode = phase_mode(phase)
        prompt, answer, family = _math_case(node, seed)
        rubric = _rubric(node, node["title"])
        params = {"competency": cid, "phase": phase, "seed": seed}
        errors = node.get("diagnostic_signals", [])

        if mode == "model":
            return open_task(
                task_id,
                f"upper.math.{family}.model",
                f"Esempio svolto: {prompt} Risposta del modello: {answer}. Spiega il controllo o il passaggio decisivo che rende valida la soluzione.",
                band,
                support,
                params=params,
                dimensions=["reasoning", "explanation", "accuracy"],
                rubric=rubric,
                acceptable="identifica il passaggio decisivo e lo collega alla soluzione mostrata",
                errors=errors,
            )
        if mode == "transfer" or answer == "valutazione tramite rubrica":
            objective = node.get("objectives", [node["title"]])[0]
            return open_task(
                task_id,
                f"upper.math.{family}.{mode}",
                f"{prompt} Motiva la strategia e collega la risposta all'obiettivo: {objective}",
                band,
                support,
                params=params,
                dimensions=["reasoning", "transfer", "independence"],
                rubric=rubric,
                acceptable=answer,
                errors=errors,
            )
        return task(
            task_id,
            f"upper.math.{family}.{mode}",
            prompt,
            answer,
            band,
            support,
            params=params,
            dimensions=["accuracy", "reasoning", "independence"],
            errors=errors,
            rubric=rubric,
        )
    return build


READING_BANK = {
    "B1": [
        ("A school introduced a quiet study room after lessons. Students can use it freely, but group work must be booked in advance. After one month, teachers noticed that more students stayed at school to finish homework.", "the school created a study space with different rules for individual and group work"),
        ("A local sports centre changed its timetable after asking teenagers for feedback. Evening sessions now start later, while weekend activities remain unchanged. The centre will review attendance after three months.", "the sports centre changed evening times after feedback and will review the result"),
    ],
    "B2": [
        ("Many cities promote cycling as a way to reduce traffic. Building cycle lanes can help, but infrastructure alone may not change habits. Researchers also point to safety, public transport links and secure parking as factors that influence whether people choose a bicycle regularly.", "cycling habits depend on several factors, not only cycle lanes"),
        ("Remote work can reduce commuting and increase flexibility, but its effects are not identical for everyone. Some employees value autonomy, while others report weaker informal collaboration. Organisations therefore need to consider both productivity and communication when designing policies.", "remote work has mixed effects and policies should balance flexibility with collaboration"),
    ],
}

LISTENING_BANK = {
    "B1": [
        ("The workshop starts at ten, but participants should arrive fifteen minutes early. Bring a notebook; all other materials will be provided.", "participants should arrive at 9:45"),
        ("The train normally leaves from platform two, but today it will depart from platform five. Passengers for the airport should board the first three carriages.", "today the train leaves from platform five"),
    ],
    "B2": [
        ("The speaker supports the new project overall, although she questions its cost. She argues that a smaller pilot would provide evidence before the organisation makes a long-term commitment.", "she supports testing the project on a smaller scale first"),
        ("The lecturer does not reject artificial intelligence in education, but warns that convenience can hide weak understanding. He recommends using it to compare ideas and receive feedback rather than to replace the student's own reasoning.", "AI should support reasoning and feedback rather than replace thinking"),
        ("The project manager says the deadline can still be met, but only if testing begins this week. She asks the team to postpone two optional features and focus first on reliability.", "the team should prioritise testing and reliability to protect the deadline"),
        ("The engineer agrees that the new system is faster, yet warns that staff need more training before it is used with customers. He recommends a short internal trial before full deployment.", "the faster system should be tested internally while staff receive training"),
    ],
}

OPEN_SCENARIOS = [
    "a school policy about phones",
    "a proposal for a local environmental project",
    "a decision about study and work experience",
    "a plan for improving public transport for young people",
]

MODEL_TEXT = {
    "spoken_interaction": "Model move: 'I see your point, but I think the rule should be more flexible because... What do you think about...?'",
    "spoken_production": "Model structure: opening claim → two developed points → brief example → conclusion.",
    "writing": "Model paragraph: 'One advantage is flexibility. However, flexibility only helps when expectations are clear. For this reason, a good policy should combine freedom with agreed deadlines.'",
    "mediation": "Model move: identify the listener's need → select only relevant information → reformulate it → check that no unsupported claim was added.",
    "learning_strategy": "Model strategy: first predict the task, then monitor comprehension, finally check errors and choose one next action.",
    "integrated_language_use": "Model sequence: understand the source → answer the purpose → reformulate the key point for another person.",
}


def _english_builder(cid: str):
    def build(phase, seed, band, support, task_id):
        node = _index("english")[cid]
        strand = node.get("strand", "integrated_language_use")
        cefr = node.get("cefr_anchor") or ("B2" if "b2" in cid else "B1")
        level = "B2" if cefr == "B2" else "B1"
        mode = phase_mode(phase)
        rng = random.Random(seed)
        rubric = _rubric(node, node["title"])
        params = {"competency": cid, "cefr": cefr, "phase": phase, "seed": seed}
        errors = node.get("diagnostic_signals", [])

        if strand == "reading":
            text, main = rng.choice(READING_BANK[level])
            if mode == "model":
                return open_task(task_id, f"upper.eng.reading.{level}.model", f"Worked example. Text: {text} Model main point: {main}. Identify two clues in the text that justify the model answer.", band, support, params=params, dimensions=["reading", "evidence_use", "explanation"], rubric=rubric, acceptable="two relevant textual clues", errors=errors)
            if mode == "transfer":
                return open_task(task_id, f"upper.eng.reading.{level}.transfer", f"Read: {text} Summarise the main point and identify one detail that supports it and one inference that would be unsafe.", band, support, params=params, dimensions=["reading", "inference", "evidence_use"], rubric=rubric, acceptable=main, errors=errors)
            return task(task_id, f"upper.eng.reading.{level}.{mode}", f"Read: {text} What is the main point?", main, band, support, params=params, dimensions=["accuracy", "reading", "gist"], rubric=rubric, errors=errors)

        if strand == "listening":
            script, answer = rng.choice(LISTENING_BANK[level])
            listen_params = dict(params, tutor_script=script)
            if mode == "model":
                return open_task(task_id, f"upper.eng.listening.{level}.model", f"After the tutor reads the script, use this model answer: '{answer}'. Explain which words or discourse signals support that answer.", band, support, params=listen_params, dimensions=["listening", "evidence_use", "explanation"], rubric=rubric, acceptable="identifies relevant listening clues", errors=errors)
            if mode == "transfer":
                return open_task(task_id, f"upper.eng.listening.{level}.transfer", "Listen twice. State the main position and one supporting detail, then explain why transcribing every word would be inefficient.", band, support, params=listen_params, dimensions=["listening", "gist", "strategy_use"], rubric=rubric, acceptable=answer, errors=errors)
            return task(task_id, f"upper.eng.listening.{level}.{mode}", "Listen to the tutor reading the text. What is the key message?", answer, band, support, params=listen_params, dimensions=["accuracy", "listening", "gist"], rubric=rubric, errors=errors)

        if strand == "grammar":
            if level == "B2":
                choices = [
                    ("Complete naturally: If the team ___ (test) the idea earlier, it might have avoided the problem.", "had tested"),
                    ("Complete naturally: The report ___ (finish) before the meeting started.", "had been finished"),
                ]
            else:
                choices = [
                    ("Complete naturally: I ___ (live) here for three years.", "have lived"),
                    ("Complete naturally: When I arrived, they ___ (wait) for the bus.", "were waiting"),
                ]
            prompt, answer = rng.choice(choices)
            if mode == "model":
                return open_task(task_id, f"upper.eng.grammar.{level}.model", f"Worked example: {prompt} Model answer: {answer}. Explain what meaning or time relationship makes this form appropriate.", band, support, params=params, dimensions=["grammar_control", "explanation", "accuracy"], rubric=rubric, acceptable="links form to meaning", errors=errors)
            if mode == "transfer":
                return open_task(task_id, f"upper.eng.grammar.{level}.transfer", prompt + " Then write a different sentence expressing the same time or hypothetical relationship.", band, support, params=params, dimensions=["accuracy", "transfer", "grammar_control"], rubric=rubric, acceptable=answer, errors=errors)
            return task(task_id, f"upper.eng.grammar.{level}.{mode}", prompt, answer, band, support, params=params, dimensions=["accuracy", "grammar_control"], rubric=rubric, errors=errors)

        if strand == "vocabulary":
            concept = rng.choice(["a useful long-term improvement", "a difficult but worthwhile decision", "a result that was not expected"])
            model = "Model paraphrases: 'a change that remains useful over time' / 'an improvement with lasting benefits'."
            prompt = (model + " Now paraphrase a different idea twice: " + concept) if mode == "model" else f"Explain '{concept}' in two different ways, choosing wording appropriate for a school or work context."
            return open_task(task_id, f"upper.eng.vocabulary.{level}.{mode}", prompt, band, support, params=params, dimensions=["vocabulary", "paraphrase", "register"], rubric=rubric, acceptable="two appropriate paraphrases", errors=errors)

        scenario = rng.choice(OPEN_SCENARIOS)
        prompts = {
            "spoken_interaction": f"Discuss {scenario}. State your view, respond to a different view, ask one clarifying question and work toward a practical conclusion.",
            "spoken_production": f"Give a short organised talk about {scenario}, with an opening, two developed points and a conclusion.",
            "writing": f"Write a connected text about {scenario}. State the purpose clearly, organise ideas in paragraphs and revise one sentence for precision or register.",
            "mediation": f"A short source concerns {scenario}. Relay the essential information to someone with a different need: select, reformulate and avoid unsupported claims.",
            "learning_strategy": f"Imagine a difficult English task about {scenario}. Describe what you would do before, during and after the task, and when you would change strategy.",
            "integrated_language_use": f"Use English to understand a short input about {scenario}, respond coherently and reformulate one key idea for another person.",
        }
        prompt = prompts.get(strand, f"Use the target English competence in a realistic situation involving {scenario} and explain one strategic choice.")
        if mode == "model":
            prompt = MODEL_TEXT.get(strand, "Model principle: make purpose, evidence and language choice explicit.") + " Then apply the same structure to: " + prompt
        return open_task(task_id, f"upper.eng.{strand}.{level}.{mode}", prompt, band, support, params=params, dimensions=["independence", "transfer", "accuracy"], rubric=rubric, acceptable="meets the communicative purpose at the target level", errors=errors)
    return build


UPPER_MATH_BUILDERS = {cid: _math_builder(cid) for cid in _index("mathematics")}
UPPER_ENGLISH_BUILDERS = {cid: _english_builder(cid) for cid in _index("english")}
