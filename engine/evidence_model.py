from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timezone
from typing import Any

OUTCOME_VALUE = {
    "correct": 1.0,
    "partially_correct": 0.6,
    "incorrect": 0.0,
    "not_completed": 0.0,
}

INDEPENDENCE_VALUE = {
    "none": 1.0,
    "light_prompt": 0.78,
    "structured_prompt": 0.48,
    "worked_support": 0.22,
    "direct_solution": 0.0,
}


def _clamp(value: float) -> float:
    return max(0.0, min(1.0, value))


def _estimate(values: list[float]) -> dict[str, float | int]:
    if not values:
        return {"value": 0.5, "confidence": 0.0, "evidence_count": 0}
    mean = sum(values) / len(values)
    confidence = min(1.0, len(values) / 5.0)
    return {
        "value": round(_clamp(mean), 4),
        "confidence": round(confidence, 4),
        "evidence_count": len(values),
    }


def _event_score(event: dict[str, Any], support_weights: dict[str, float]) -> float | None:
    status = event.get("outcome", {}).get("status")
    if status not in OUTCOME_VALUE:
        return None
    base = OUTCOME_VALUE[status]
    support_level = event.get("support", {}).get("level", "none")
    return base * float(support_weights.get(support_level, 1.0))


def _success_streak(scores: list[float], successful: bool) -> int:
    count = 0
    for score in reversed(scores):
        condition = score >= 0.6 if successful else score < 0.6
        if not condition:
            break
        count += 1
    return count


def _hypotheses(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, str | None], list[tuple[str, float]]] = defaultdict(list)
    for event in events:
        event_id = str(event.get("event_id", "unknown"))
        for observation in event.get("error_observations", []):
            code = observation.get("code")
            if not code or code == "other":
                continue
            related = observation.get("related_competency_id")
            observer_conf = float(observation.get("observer_confidence", 0.5))
            grouped[(code, related)].append((event_id, observer_conf))

    result: list[dict[str, Any]] = []
    for (code, related), observations in grouped.items():
        count = len(observations)
        average = sum(conf for _, conf in observations) / count
        recurrence_boost = min(1.0, 0.75 + 0.12 * (count - 1))
        confidence = _clamp(average * recurrence_boost)
        persistence = "single" if count == 1 else "repeated" if count < 4 else "persistent"
        item: dict[str, Any] = {
            "code": code,
            "confidence": round(confidence, 4),
            "persistence": persistence,
            "evidence_for": [event_id for event_id, _ in observations],
            "evidence_against": [],
        }
        if related:
            item["related_competency_id"] = related
        result.append(item)

    return sorted(result, key=lambda item: item["confidence"], reverse=True)


def aggregate_competency_state(
    competency_id: str,
    events: list[dict[str, Any]],
    policy: dict[str, Any],
) -> dict[str, Any]:
    """Build a reproducible state estimate from immutable evidence events.

    This is an engineering baseline for TutorLab v0.1, not a psychometric model.
    Unknown dimensions keep confidence zero rather than being treated as weak skills.
    """

    relevant = [event for event in events if event.get("competency_id") == competency_id]
    relevant.sort(key=lambda event: event.get("observed_at", ""))

    support_weights = policy.get("supported_success_weights", {})
    scores: list[float] = []
    independence: list[float] = []
    transfer: list[float] = []
    explanation: list[float] = []
    fluency: list[float] = []

    for event in relevant:
        score = _event_score(event, support_weights)
        if score is not None:
            scores.append(score)

        level = event.get("support", {}).get("level", "none")
        if event.get("outcome", {}).get("status") in {"correct", "partially_correct"}:
            independence.append(INDEPENDENCE_VALUE.get(level, 0.5))

        transfer_value = event.get("outcome", {}).get("transfer_success")
        if transfer_value is not None:
            transfer.append(float(transfer_value))
        elif event.get("task", {}).get("context_familiarity") in {"near_transfer", "farther_transfer"} and score is not None:
            transfer.append(score)

        explanation_value = event.get("outcome", {}).get("explanation_quality")
        if explanation_value is not None:
            explanation.append(float(explanation_value))

        tags = set(event.get("tags", []))
        if "fluency_ok" in tags:
            fluency.append(1.0)
        elif "fluency_slow" in tags:
            fluency.append(0.35)

    stability_values = [] if len(scores) <= 1 else [1.0 - abs(a - b) for a, b in zip(scores, scores[1:])]

    accuracy_estimate = _estimate(scores)
    independence_estimate = _estimate(independence)
    stability_estimate = _estimate(stability_values)
    transfer_estimate = _estimate(transfer)
    explanation_estimate = _estimate(explanation)
    fluency_estimate = _estimate(fluency)

    estimates = [
        accuracy_estimate,
        independence_estimate,
        stability_estimate,
        transfer_estimate,
        explanation_estimate,
        fluency_estimate,
    ]
    coverage = sum(1 for item in estimates if item["confidence"] > 0) / len(estimates)
    event_factor = min(1.0, len(relevant) / 6.0)
    confidence = round(_clamp(0.65 * event_factor + 0.35 * coverage), 4)

    hypotheses = _hypotheses(relevant)
    raw_success = [
        OUTCOME_VALUE[event.get("outcome", {}).get("status")]
        for event in relevant
        if event.get("outcome", {}).get("status") in OUTCOME_VALUE
    ]
    if len(raw_success) < 3:
        contradiction = 0.0
    else:
        success_rate = sum(1 for value in raw_success if value >= 0.6) / len(raw_success)
        outcome_variability = 4 * success_rate * (1 - success_rate)
        strongest_explanation = hypotheses[0]["confidence"] if hypotheses else 0.0
        contradiction = round(_clamp(outcome_variability * (1 - 0.75 * strongest_explanation)), 4)

    if confidence < 0.35:
        status = "unknown"
    elif accuracy_estimate["value"] < 0.5:
        status = "emerging"
    elif accuracy_estimate["value"] < 0.8 or independence_estimate["value"] < 0.65:
        status = "developing"
    elif transfer_estimate["confidence"] >= 0.4 and transfer_estimate["value"] >= 0.7:
        status = "extended"
    else:
        status = "secure"

    observed_times = [event.get("observed_at") for event in relevant if event.get("observed_at")]
    independent_count = sum(1 for event in relevant if event.get("support", {}).get("level") == "none")
    transfer_count = sum(
        1
        for event in relevant
        if event.get("outcome", {}).get("transfer_success") is not None
        or event.get("task", {}).get("context_familiarity") in {"near_transfer", "farther_transfer"}
    )

    evidence_summary: dict[str, Any] = {
        "event_count": len(relevant),
        "independent_event_count": independent_count,
        "transfer_event_count": transfer_count,
        "recent_success_streak": _success_streak(raw_success, True),
        "recent_failure_streak": _success_streak(raw_success, False),
        "contradiction_level": contradiction,
    }
    if observed_times:
        evidence_summary["first_observed_at"] = observed_times[0]
        evidence_summary["last_observed_at"] = observed_times[-1]

    return {
        "version": "0.1",
        "competency_id": competency_id,
        "mastery": {
            "accuracy": accuracy_estimate,
            "independence": independence_estimate,
            "stability": stability_estimate,
            "transfer": transfer_estimate,
            "explanation": explanation_estimate,
            "fluency": fluency_estimate,
        },
        "confidence": confidence,
        "status": status,
        "evidence_summary": evidence_summary,
        "error_hypotheses": hypotheses,
        "updated_at": observed_times[-1] if observed_times else datetime.now(timezone.utc).isoformat(),
    }
