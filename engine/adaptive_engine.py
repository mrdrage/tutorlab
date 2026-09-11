from __future__ import annotations

from dataclasses import dataclass
from typing import Any

ACTIONS = {"recover", "consolidate", "advance", "extend", "reassess"}


@dataclass(frozen=True)
class Decision:
    action: str
    confidence: float
    rationale: str
    next_competency_id: str | None = None
    recovery_competency_id: str | None = None


def _meets(values: dict[str, float], thresholds: dict[str, float]) -> bool:
    return all(float(values.get(key, 0.0)) >= float(value) for key, value in thresholds.items())


def _primary_hypothesis(state: dict[str, Any]) -> dict[str, Any] | None:
    hypotheses = state.get("error_hypotheses", [])
    if not hypotheses:
        return None
    return max(hypotheses, key=lambda item: float(item.get("confidence", 0.0)))


def decide(
    target_state: dict[str, Any],
    policy: dict[str, Any],
    *,
    current_target_id: str,
    suggested_next_id: str | None = None,
    recovery_depth: int = 0,
) -> Decision:
    """Return a transparent routing decision from an already-computed competency state.

    This v0.1 function deliberately does not infer clinical conditions, mutate evidence,
    or hide the policy behind a learned model.
    """

    confidence = float(target_state.get("confidence", 0.0))
    evidence = target_state.get("evidence_summary", {})
    contradiction = float(evidence.get("contradiction_level", 0.0))
    min_conf = float(policy["min_decision_confidence"])

    if confidence < min_conf or contradiction >= 0.6:
        return Decision(
            action="reassess",
            confidence=max(0.35, confidence),
            rationale="Evidenze insufficienti o contraddittorie: serve una prova mirata prima di cambiare percorso.",
        )

    hypothesis = _primary_hypothesis(target_state)
    strong_error = float(policy["strong_error_hypothesis"])

    if hypothesis:
        code = hypothesis.get("code")
        h_conf = float(hypothesis.get("confidence", 0.0))
        related = hypothesis.get("related_competency_id")

        if (
            code == "missing_prerequisite"
            and h_conf >= strong_error
            and related
        ):
            if recovery_depth >= int(policy["max_recovery_depth"]):
                return Decision(
                    action="reassess",
                    confidence=h_conf,
                    rationale="La lacuna sembra risalire oltre la profondità di recupero consentita; servono nuove evidenze prima di scendere ancora.",
                )
            return Decision(
                action="recover",
                confidence=h_conf,
                rationale=f"Un prerequisito specifico ({related}) spiega con confidenza alta il fallimento sull'obiettivo corrente.",
                recovery_competency_id=related,
            )

        if code in set(policy["block_advance_errors"]) and h_conf >= strong_error:
            return Decision(
                action="consolidate",
                confidence=h_conf,
                rationale=f"L'ipotesi {code} è abbastanza forte da bloccare l'avanzamento, ma non identifica un prerequisito più specifico da recuperare.",
                next_competency_id=current_target_id,
            )

    mastery = target_state.get("mastery", {})
    independent = int(evidence.get("independent_event_count", 0))

    if _meets(mastery | {"confidence": confidence}, policy["extend"]):
        return Decision(
            action="extend",
            confidence=confidence,
            rationale="La competenza è accurata, autonoma, stabile e trasferibile: è appropriato aumentare apertura e profondità.",
            next_competency_id=current_target_id,
        )

    if (
        independent >= int(policy["min_independent_for_advance"])
        and _meets(mastery | {"confidence": confidence}, policy["advance"])
    ):
        return Decision(
            action="advance",
            confidence=confidence,
            rationale="Le evidenze autonome e multidimensionali sono sufficienti per tentare il nodo successivo.",
            next_competency_id=suggested_next_id,
        )

    return Decision(
        action="consolidate",
        confidence=confidence,
        rationale="La competenza mostra basi utili ma non soddisfa ancora i criteri di autonomia, stabilità e trasferimento per avanzare.",
        next_competency_id=current_target_id,
    )
