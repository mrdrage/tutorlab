#!/usr/bin/env python3
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from engine.adaptive_engine import decide
from engine.evidence_model import aggregate_competency_state


def load(path):
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def main():
    policy = load(ROOT / "config/adaptive-policy.json")
    suite = load(ROOT / "tests/adaptive/scenarios.json")
    errors = []

    for scenario in suite["scenarios"]:
        result = decide(
            scenario["state"], policy,
            current_target_id=scenario["target"],
            suggested_next_id=scenario.get("next"),
            recovery_depth=scenario.get("recovery_depth", 0),
        )
        if result.action != scenario["expected"]:
            errors.append(f"{scenario['id']}: {result.action} != {scenario['expected']}")
        if scenario.get("expected_recovery") and result.recovery_competency_id != scenario["expected_recovery"]:
            errors.append(f"{scenario['id']}: recovery target errato")

    events = []
    for i, status in enumerate(["incorrect", "partially_correct", "incorrect", "partially_correct"], 1):
        events.append({
            "event_id": f"e{i}",
            "competency_id": "math.numbers.proportions",
            "observed_at": f"2026-09-1{i}T10:00:00+02:00",
            "task": {"task_id": f"t{i}", "mode": "diagnostic", "context_familiarity": "near_transfer"},
            "outcome": {"status": status, "transfer_success": 0.2, "explanation_quality": 0.35},
            "support": {"level": "none"},
            "error_observations": [{
                "code": "missing_prerequisite",
                "description": "ratio setup error",
                "related_competency_id": "math.numbers.ratios",
                "observer_confidence": 0.9
            }]
        })

    state = aggregate_competency_state("math.numbers.proportions", events, policy)
    result = decide(state, policy, current_target_id="math.numbers.proportions", suggested_next_id="math.numbers.percentages")
    if result.action != "recover" or result.recovery_competency_id != "math.numbers.ratios":
        errors.append("pipeline evidence-state-decision non produce recover ratios")
    if state["mastery"]["fluency"]["confidence"] != 0.0:
        errors.append("dimensione non osservata con confidenza non nulla")

    if errors:
        print("Adaptive engine validation: FAILED")
        for error in errors:
            print("-", error)
        return 1

    print("Adaptive engine validation: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
