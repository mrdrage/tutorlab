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

    if "derivative" in cid or "derivat" in cid:
        a = rng.choice([2, 3, 4])
        b = rng.choice([1, 2, 5])
        return (f"Per f(x)={a}x^2+{b}x, determina f'(x).", f"{2*a}x+{b}", "calculus")
    if "integral" in cid or "integr" in cid:
        a = rng.choice([2, 4, 6])
        return (f"Calcola una primitiva di f(x)={a}x.", f"{a//2}x^2+C", "calculus")
    if "limit" in cid or "analysis" in cid:
        a = rng.choice([2, 3, 5])
        return (f"Calcola lim x→{a} di (x^2-{a*a})/(x-{a}).", str(2*a), "calculus")
    if strand == "trigonometry" or "trigon" in cid:
        return ("In un triangolo rettangolo, rispetto all'angolo α il cateto opposto misura 3 e l'ipotenusa 5. Calcola sin α.", "3/5", "trigonometry")
    if strand in {"exponential_log", "exponential_logarithmic"} or "explog" in cid or "logarith" in cid:
        base = rng.choice([2, 3, 10])
        exp = rng.choice([2, 3])
        value = base ** exp
        return (f"Risolvi {base}^x={value}.", str(exp), "exponential_log")
    if strand == "sequences" or "sequence" in cid:
        start = rng.choice([2, 3, 5])
        step = rng.choice([2, 4, 5])
        return (f"La successione inizia {start}, {start+step}, {start+2*step}. Qual è il termine successivo?", str(start+3*step), "sequences")
    if strand in {"statistics_probability", "data_probability"} or "probability" in cid or "statistic" in cid:
        values = [2, 4, 4, 6, 9]
        return (f"Dati {values}, determina la mediana.", "4", "statistics_probability")
    if strand in {"geometry", "analytic_geometry"} or "geometry" in cid:
        return ("Nel piano cartesiano A=(0,0) e B=(3,4). Calcola la distanza AB.", "5", "geometry")
    if strand == "functions" or "function" in cid:
        m = rng.choice([2, 3, -2])
        q = rng.choice([1, 4, -1])
        x = rng.choice([2, 3])
        return (f"Per f(x)={m}x+({q}), calcola f({x}).", str(m*x+q), "functions")
    if strand in {"equations_inequalities", "algebra"} or "algebra" in cid or "equation" in cid or "inequal" in cid:
        if "quadratic" in cid:
            return ("Risolvi x^2-5x+6=0.", "x=2 oppure x=3", "quadratic")
        if "inequal" in cid:
            return ("Risolvi 3x+2<11.", "x<3", "inequality")
        return ("Risolvi 3x+5=17 e verifica la soluzione.", "x=4", "algebra")
    return ("Spiega quale rappresentazione useresti per confrontare due modelli quantitativi e perché.", "valutazione tramite rubrica", "modelling")


def _math_builder(cid: str):
    def build(phase, seed, band, support, task_id):
        node = _index("mathematics")[cid]
        mode = phase_mode(phase)
        prompt, answer, family = _math_case(node, seed)
        dimensions = ["accuracy", "reasoning", "independence"]
        if mode in {"transfer", "model"} or answer == "valutazione tramite rubrica":
            objective = node.get("objectives", [node["title"]])[0]
            lead = "Osserva il modello e rendi espliciti i passaggi. " if mode == "model" else "Applica la competenza in una forma meno familiare. "
            return open_task(
                task_id,
                f"upper.math.{family}.{mode}",
                lead + prompt + f" Collega la risposta all'obiettivo: {objective}",
                band,
                support,
                params={"competency": cid, "phase": phase, "seed": seed},
                dimensions=["reasoning", "transfer", "independence"],
                rubric=_rubric(node, node["title"]),
                acceptable=answer,
                errors=node.get("diagnostic_signals", []),
            )
        return task(
            task_id,
            f"upper.math.{family}.{mode}",
            prompt,
            answer,
            band,
            support,
            params={"competency": cid, "phase": phase, "seed": seed},
            dimensions=dimensions,
            errors=node.get("diagnostic_signals", []),
            rubric=_rubric(node, node["title"]),
        )
    return build


READING_BANK = {
    "B1": (
        "A school introduced a quiet study room after lessons. Students can use it freely, but group work must be booked in advance. After one month, teachers noticed that more students stayed at school to finish homework.",
        "the school created a study space with different rules for individual and group work",
    ),
    "B2": (
        "Many cities promote cycling as a way to reduce traffic. Building cycle lanes can help, but infrastructure alone may not change habits. Researchers also point to safety, public transport links and secure parking as factors that influence whether people choose a bicycle regularly.",
        "cycling habits depend on several factors, not only cycle lanes",
    ),
}

LISTENING_BANK = {
    "B1": ("The workshop starts at ten, but participants should arrive fifteen minutes early. Bring a notebook; all other materials will be provided.", "participants should arrive at 9:45"),
    "B2": ("The speaker supports the new project overall, although she questions its cost. She argues that a smaller pilot would provide evidence before the organisation makes a long-term commitment.", "she supports testing the project on a smaller scale first"),
}


def _english_builder(cid: str):
    def build(phase, seed, band, support, task_id):
        node = _index("english")[cid]
        strand = node.get("strand", "integrated_language_use")
        cefr = node.get("cefr_anchor") or ("B2" if "b2" in cid else "B1")
        mode = phase_mode(phase)
        rubric = _rubric(node, node["title"])
        common = dict(params={"competency": cid, "cefr": cefr, "phase": phase, "seed": seed}, errors=node.get("diagnostic_signals", []))

        if strand == "reading":
            text, main = READING_BANK["B2" if cefr == "B2" else "B1"]
            if mode == "transfer":
                return open_task(task_id, f"upper.eng.reading.{cefr}.{mode}", f"Read: {text} Summarise the main point and identify one detail that supports it.", band, support, dimensions=["reading", "inference", "evidence_use"], rubric=rubric, acceptable=main, **common)
            return task(task_id, f"upper.eng.reading.{cefr}.{mode}", f"Read: {text} What is the main point?", main, band, support, dimensions=["accuracy", "reading", "gist"], rubric=rubric, **common)

        if strand == "listening":
            script, answer = LISTENING_BANK["B2" if cefr == "B2" else "B1"]
            params = dict(common["params"], tutor_script=script)
            if mode == "transfer":
                return open_task(task_id, f"upper.eng.listening.{cefr}.{mode}", "Listen to the tutor reading the text twice. State the main position and one supporting detail without trying to transcribe every word.", band, support, params=params, dimensions=["listening", "gist", "detail"], rubric=rubric, acceptable=answer, errors=common["errors"])
            return task(task_id, f"upper.eng.listening.{cefr}.{mode}", "Listen to the tutor reading the text. What is the key message?", answer, band, support, params=params, dimensions=["accuracy", "listening", "gist"], rubric=rubric, errors=common["errors"])

        if strand == "grammar":
            if cefr == "B2":
                prompt = "Complete naturally: If the team ___ (test) the idea earlier, it might have avoided the problem."
                answer = "had tested"
            else:
                prompt = "Complete naturally: I ___ (live) here for three years."
                answer = "have lived"
            if mode == "transfer":
                return open_task(task_id, f"upper.eng.grammar.{cefr}.{mode}", prompt + " Then write one different sentence expressing the same time or hypothetical relationship.", band, support, dimensions=["accuracy", "transfer", "grammar_control"], rubric=rubric, acceptable=answer, **common)
            return task(task_id, f"upper.eng.grammar.{cefr}.{mode}", prompt, answer, band, support, dimensions=["accuracy", "grammar_control"], rubric=rubric, **common)

        if strand == "vocabulary":
            return open_task(task_id, f"upper.eng.vocabulary.{cefr}.{mode}", "Explain the idea 'a useful long-term improvement' in two different ways, choosing wording appropriate for a school or work context.", band, support, dimensions=["vocabulary", "paraphrase", "register"], rubric=rubric, acceptable="two appropriate paraphrases", **common)

        prompts = {
            "spoken_interaction": "Discuss a proposal to change one school rule. State your view, respond to a different view, ask one clarifying question and work toward a practical conclusion.",
            "spoken_production": "Give a short organised talk on a familiar social or study-related topic, with an opening, two developed points and a conclusion.",
            "writing": "Write a connected text appropriate to the target level. State the purpose clearly, organise ideas in paragraphs and revise one sentence for precision or register.",
            "mediation": "Relay the essential information from a short source to someone with a different need. Select, reformulate and avoid adding unsupported claims.",
            "learning_strategy": "Describe which strategy you would use before, during and after a difficult English task, and explain when you would change strategy.",
            "integrated_language_use": "Use English to understand a short input, respond coherently and reformulate one key idea for another person.",
        }
        prompt = prompts.get(strand, "Use the target English competence in a realistic study, work or everyday situation and explain one strategic choice.")
        return open_task(task_id, f"upper.eng.{strand}.{cefr}.{mode}", prompt, band, support, dimensions=["independence", "transfer", "accuracy"], rubric=rubric, acceptable="meets the communicative purpose at the target level", **common)
    return build


UPPER_MATH_BUILDERS = {cid: _math_builder(cid) for cid in _index("mathematics")}
UPPER_ENGLISH_BUILDERS = {cid: _english_builder(cid) for cid in _index("english")}
