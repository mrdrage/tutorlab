from __future__ import annotations

from typing import Any

DIMENSIONS = ("accuracy", "independence", "stability", "transfer", "explanation", "fluency")


def _dimension_confidence(state: dict[str, Any], dimension: str) -> float:
    raw = state.get("mastery", {}).get(dimension, 0.0)
    if isinstance(raw, dict):
        return float(raw.get("confidence", 0.0))
    return float(state.get("confidence", 0.0))


def plan_reassessment(
    state: dict[str, Any],
    *,
    target_competency_id: str,
    min_decision_confidence: float = 0.55,
) -> dict[str, Any]:
    """Plan evidence-gathering probes, not exercise text.

    Content generation belongs to the future session/generation engine. This planner
    only states what uncertainty a diagnostic task should resolve.
    """

    overall = float(state.get("confidence", 0.0))
    contradiction = float(state.get("evidence_summary", {}).get("contradiction_level", 0.0))
    hypotheses = sorted(
        state.get("error_hypotheses", []),
        key=lambda item: float(item.get("confidence", 0.0)),
        reverse=True,
    )

    questions: list[str] = []
    probes: list[dict[str, Any]] = []

    if overall < min_decision_confidence:
        questions.append("La prestazione osservata è rappresentativa o abbiamo ancora troppo poche evidenze?")
        probes.append({
            "competency_id": target_competency_id,
            "purpose": "baseline_independent",
            "support": "none",
            "variation": "same_concept_new_instance",
        })

    if contradiction >= 0.6:
        questions.append("La variabilità dipende dal contesto, dalla rappresentazione o da instabilità reale?")
        probes.extend([
            {
                "competency_id": target_competency_id,
                "purpose": "representation_check",
                "support": "none",
                "variation": "alternate_representation",
            },
            {
                "competency_id": target_competency_id,
                "purpose": "near_transfer_check",
                "support": "none",
                "variation": "near_transfer",
            },
        ])

    if hypotheses:
        primary = hypotheses[0]
        related = primary.get("related_competency_id")
        h_conf = float(primary.get("confidence", 0.0))
        if primary.get("code") == "missing_prerequisite" and related and h_conf >= 0.45:
            questions.append(f"Il prerequisito {related} spiega il fallimento sull'obiettivo corrente?")
            probes.append({
                "competency_id": related,
                "purpose": "prerequisite_probe",
                "support": "light_prompt",
                "variation": "minimal_clean_probe",
            })

    low_dimensions = [dimension for dimension in DIMENSIONS if _dimension_confidence(state, dimension) < 0.4]
    for dimension in low_dimensions[:2]:
        if dimension == "transfer":
            probes.append({
                "competency_id": target_competency_id,
                "purpose": "measure_transfer",
                "support": "none",
                "variation": "near_transfer",
            })
            questions.append("La competenza regge quando cambia il contesto?")
        elif dimension == "independence":
            probes.append({
                "competency_id": target_competency_id,
                "purpose": "measure_independence",
                "support": "none",
                "variation": "familiar_context",
            })
            questions.append("Lo studente riesce senza prompt o struttura esterna?")
        elif dimension == "explanation":
            probes.append({
                "competency_id": target_competency_id,
                "purpose": "measure_explanation",
                "support": "none",
                "variation": "explain_reasoning",
            })
            questions.append("Lo studente sa spiegare la scelta o il procedimento?")

    unique: list[dict[str, Any]] = []
    seen = set()
    for probe in probes:
        key = (probe["competency_id"], probe["purpose"], probe["variation"])
        if key not in seen:
            seen.add(key)
            unique.append(probe)

    if not unique:
        unique.append({
            "competency_id": target_competency_id,
            "purpose": "confirmation_probe",
            "support": "none",
            "variation": "new_instance",
        })
        questions.append("La decisione preliminare resta valida su una nuova evidenza indipendente?")

    return {
        "target_competency_id": target_competency_id,
        "questions_to_resolve": questions,
        "probes": unique[:4],
    }
