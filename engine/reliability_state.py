from __future__ import annotations

from copy import deepcopy
from typing import Any

from engine.evidence_model import OUTCOME_VALUE, aggregate_competency_state


def _clamp(value: float) -> float:
    return max(0.0, min(1.0, value))


def _later_clean_successes(events: list[dict[str, Any]], evidence_for: list[str]) -> list[str]:
    positions = {str(event.get("event_id", "")): index for index, event in enumerate(events)}
    known_positions = [positions[event_id] for event_id in evidence_for if event_id in positions]
    if not known_positions:
        return []
    last = max(known_positions)
    result = []
    for event in events[last + 1 :]:
        status = event.get("outcome", {}).get("status")
        support = event.get("support", {}).get("level", "none")
        if status == "correct" and support in {"none", "light_prompt"}:
            result.append(str(event.get("event_id", "unknown")))
    return result


def _alternation_score(raw_success: list[float], window: int) -> float:
    recent = raw_success[-max(4, window) :]
    if len(recent) < 4:
        return 0.0
    binary = [1 if value >= 0.6 else 0 for value in recent]
    rate = sum(binary) / len(binary)
    balance = 4 * rate * (1 - rate)
    flips = sum(a != b for a, b in zip(binary, binary[1:])) / max(1, len(binary) - 1)
    return _clamp(balance * flips)


def calibrated_state(competency_id: str, events: list[dict[str, Any]], policy: dict[str, Any]) -> dict[str, Any]:
    lifetime = [event for event in events if event.get("competency_id") == competency_id]
    lifetime.sort(key=lambda event: event.get("observed_at", ""))

    window = int(policy.get("mastery_evidence_window", 0) or 0)
    active = lifetime[-window:] if window and len(lifetime) > window else lifetime
    state = deepcopy(aggregate_competency_state(competency_id, active, policy))

    decay = float(policy.get("hypothesis_clean_success_decay", 0.65))
    hypotheses = []
    for item in state.get("error_hypotheses", []):
        adjusted = dict(item)
        against = _later_clean_successes(active, list(item.get("evidence_for", [])))
        adjusted["evidence_against"] = against[-6:]
        adjusted["confidence"] = round(_clamp(float(item.get("confidence", 0.0)) * (decay ** len(against))), 4)
        hypotheses.append(adjusted)
    hypotheses.sort(key=lambda item: item.get("confidence", 0.0), reverse=True)

    raw_success = [
        OUTCOME_VALUE[event.get("outcome", {}).get("status")]
        for event in active
        if event.get("outcome", {}).get("status") in OUTCOME_VALUE
    ]
    alternation = _alternation_score(raw_success, int(policy.get("contradiction_window", 8)))
    strongest = float(hypotheses[0].get("confidence", 0.0)) if hypotheses else 0.0

    state["version"] = "0.2"
    state["error_hypotheses"] = hypotheses
    summary = dict(state.get("evidence_summary", {}))
    summary["contradiction_level"] = round(_clamp(alternation * (1 - 0.65 * strongest)), 4)
    summary["lifetime_event_count"] = len(lifetime)
    summary["active_window_event_count"] = len(active)
    state["evidence_summary"] = summary
    return state
