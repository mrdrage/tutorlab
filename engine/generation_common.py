from __future__ import annotations

MODEL_PHASES={"worked_example","targeted_model"}
GUIDED_PHASES={"guided_practice","faded_practice"}
CHECK_PHASES={"diagnostic_check","retrieval","activation","contrast_task"}
INDEPENDENT_PHASES={"independent_practice","verification","reassessment"}
TRANSFER_PHASES={"transfer","transfer_probe","challenge","strategy_comparison","explanation","reflection"}


def phase_mode(phase):
    if phase in MODEL_PHASES: return "model"
    if phase in GUIDED_PHASES: return "guided"
    if phase in CHECK_PHASES: return "check"
    if phase in TRANSFER_PHASES: return "transfer"
    return "independent"


def task(task_id,family_id,prompt,answer,band,support,*,response_mode="short_answer",params=None,dimensions=None,errors=None,rubric=None,extra_solution=None):
    solution={"answer":answer}
    if extra_solution: solution.update(extra_solution)
    return {
        "task_id":task_id,
        "family_id":family_id,
        "prompt":prompt,
        "response_mode":response_mode,
        "challenge_band":band,
        "support_level":support,
        "solution":solution,
        "rubric":rubric or {"full_credit":"Risposta corretta e ragionamento coerente con la richiesta."},
        "evidence_dimensions":dimensions or ["accuracy"],
        "error_signals":errors or [],
        "generation_parameters":params or {},
    }


def open_task(task_id,family_id,prompt,band,support,*,params=None,dimensions=None,rubric=None,acceptable=None,errors=None):
    return task(
        task_id,family_id,prompt,acceptable or "valutazione tramite rubrica",band,support,
        response_mode="open_response",params=params,dimensions=dimensions or ["explanation","transfer"],errors=errors,
        rubric=rubric or {"full_credit":"Risposta pertinente, comprensibile e motivata; applica correttamente la competenza osservata."},
    )
