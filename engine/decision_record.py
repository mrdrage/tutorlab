from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from engine.adaptive_engine import Decision


def build_decision_record(
    decision: Decision,
    *,
    target_competency_id: str,
    evidence_refs: list[str],
    primary_hypothesis: dict[str, Any] | None = None,
    objective_stack: dict[str, Any] | None = None,
    diagnostic_plan: dict[str, Any] | None = None,
    return_condition: str | None = None,
    created_at: str | None = None,
) -> dict[str, Any]:
    if not evidence_refs:
        raise ValueError("Una decisione persistita deve citare almeno una evidenza")

    record: dict[str, Any] = {
        "version": "0.1",
        "decision_id": f"decision-{uuid4()}",
        "target_competency_id": target_competency_id,
        "action": decision.action,
        "confidence": round(float(decision.confidence), 4),
        "rationale": decision.rationale,
        "evidence_refs": list(dict.fromkeys(evidence_refs)),
        "created_at": created_at or datetime.now(timezone.utc).isoformat(),
    }

    if primary_hypothesis:
        record["primary_hypothesis"] = {
            "code": primary_hypothesis.get("code", "none"),
            "confidence": float(primary_hypothesis.get("confidence", 0.0)),
        }
        related = primary_hypothesis.get("related_competency_id")
        if related:
            record["primary_hypothesis"]["related_competency_id"] = related

    if decision.next_competency_id:
        record["next_competency_id"] = decision.next_competency_id

    if decision.action == "recover":
        if not decision.recovery_competency_id:
            raise ValueError("Una decisione recover richiede recovery_competency_id")
        stack_ids = []
        depth = 1
        if objective_stack:
            frames = objective_stack.get("frames", [])
            stack_ids = [str(frame["competency_id"]) for frame in frames]
            depth = sum(1 for frame in frames if frame.get("kind") == "recovery") + 1
        record["recovery"] = {
            "suspended_target_id": target_competency_id,
            "recovery_competency_id": decision.recovery_competency_id,
            "return_condition": return_condition or "Raccogliere nuove evidenze sufficienti sul prerequisito e poi rivalutare l'obiettivo sospeso.",
            "recovery_depth": depth,
            "objective_stack": stack_ids or [target_competency_id, decision.recovery_competency_id],
        }

    if decision.action == "reassess":
        if not diagnostic_plan:
            raise ValueError("Una decisione reassess richiede un diagnostic_plan")
        record["reassessment_plan"] = {
            "questions_to_resolve": diagnostic_plan.get("questions_to_resolve", []),
            "evidence_needed": [
                f"{probe['purpose']}:{probe['competency_id']}:{probe['variation']}"
                for probe in diagnostic_plan.get("probes", [])
            ],
        }

    return record
