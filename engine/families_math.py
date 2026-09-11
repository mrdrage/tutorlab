from fractions import Fraction
import random


def _task(task_id, family_id, prompt, solution, band, support, mode="short_answer", params=None, dimensions=None, errors=None):
    return {
        "task_id": task_id,
        "family_id": family_id,
        "prompt": prompt,
        "response_mode": mode,
        "challenge_band": band,
        "support_level": support,
        "solution": solution,
        "rubric": {"full_credit": "Risposta corretta e coerente con la richiesta."},
        "evidence_dimensions": dimensions or ["accuracy"],
        "error_signals": errors or [],
        "generation_parameters": params or {},
    }


def fraction_equivalence_task(phase, seed, band, support, task_id):
    rng = random.Random(seed)
    coprime = [(2, 3), (3, 4), (3, 5), (4, 5), (5, 6), (5, 7), (7, 8)]
    n, d = rng.choice(coprime)
    factor = rng.choice([2, 3, 4, 5])
    t = rng.choice([1, 2, 3])

    if phase in {"diagnostic_check", "retrieval", "activation", "contrast_task"}:
        correct = f"{n * factor}/{d * factor}"
        distractors = [f"{n + factor}/{d + factor}", f"{n * factor}/{d}", f"{n}/{d * factor}"]
        options = [correct] + distractors
        rng.shuffle(options)
        prompt = f"Quale frazione è equivalente a {n}/{d}? " + " | ".join(options)
        return _task(task_id, "math.fraction.equivalent-choice", prompt, {"answer": correct}, band, support, "single_choice", {"n": n, "d": d, "factor": factor}, ["accuracy", "conceptual_understanding"], [{"pattern": "add_same_number", "code": "conceptual_error"}])

    if phase in {"worked_example", "targeted_model"}:
        prompt = f"Studia l'esempio: semplifica {n * factor}/{d * factor}. Dividi numeratore e denominatore per {factor}."
        return _task(task_id, "math.fraction.worked-simplification", prompt, {"steps": [f"({n * factor}÷{factor})/({d * factor}÷{factor})", f"{n}/{d}"], "answer": f"{n}/{d}"}, band, "worked_support", "structured_steps", {"n": n, "d": d, "factor": factor}, ["explanation", "procedure"])

    if phase in {"guided_practice", "faded_practice"}:
        prompt = f"Completa: {n}/{d} = {n * factor}/__ . Quale operazione fai al denominatore?"
        return _task(task_id, "math.fraction.complete-equivalent", prompt, {"answer": d * factor, "reason": f"moltiplicare per {factor}"}, band, support, "structured_steps", {"n": n, "d": d, "factor": factor}, ["accuracy", "independence", "explanation"])

    if phase in {"independent_practice", "verification", "reassessment"}:
        scale = rng.choice([2, 3, 4, 5])
        a, b = n * scale, d * scale
        prompt = f"Riduci {a}/{b} ai minimi termini e indica il divisore usato."
        return _task(task_id, "math.fraction.simplify-independent", prompt, {"answer": f"{n}/{d}", "divisor": scale}, band, support, "structured_steps", {"a": a, "b": b, "scale": scale}, ["accuracy", "independence", "procedure"])

    if phase in {"transfer", "transfer_probe", "challenge"}:
        wrong_n, wrong_d = n + t, d + t
        prompt = f"Uno studente dice che {n}/{d} = {wrong_n}/{wrong_d} perché ha aggiunto {t} sopra e sotto. Decidi se è corretto e giustifica con un criterio matematico."
        return _task(task_id, "math.fraction.error-analysis", prompt, {"answer": "non corretto", "key_idea": "per ottenere una frazione equivalente si moltiplicano o dividono entrambi i termini per lo stesso fattore non nullo"}, band, support, "open_response", {"n": n, "d": d, "t": t}, ["transfer", "explanation", "conceptual_understanding"], [{"pattern": "accept_additive_equivalence", "code": "conceptual_error"}])

    if phase in {"strategy_comparison", "explanation", "reflection"}:
        prompt = f"Spiega due modi per verificare che {n}/{d} e {n * factor}/{d * factor} rappresentino lo stesso numero."
        return _task(task_id, "math.fraction.strategy-explanation", prompt, {"acceptable": ["semplificazione", "prodotti incrociati", "stessa posizione sulla retta"]}, band, support, "open_response", {"n": n, "d": d, "factor": factor}, ["explanation", "transfer"])

    return fraction_equivalence_task("independent_practice", seed, band, support, task_id)
