#!/usr/bin/env python3
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from engine.adaptive_engine import decide
from engine.diagnostic_planner import plan_reassessment
from engine.evidence_model import aggregate_competency_state
from engine.objective_stack import complete_current, current_objective, push_recovery, recovery_depth, start_objective


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

    diagnostic = plan_reassessment(state, target_competency_id="math.numbers.proportions")
    if not any(probe["competency_id"] == "math.numbers.ratios" for probe in diagnostic["probes"]):
        errors.append("diagnostic planner non verifica il prerequisito sospetto")

    stack = start_objective("math.numbers.proportions")
    stack = push_recovery(stack, "math.numbers.ratios", reason="missing prerequisite", max_depth=2)
    stack = push_recovery(stack, "math.numbers.fraction-equivalence", reason="ratio representation unstable", max_depth=2)
    if recovery_depth(stack) != 2 or current_objective(stack) != "math.numbers.fraction-equivalence":
        errors.append("objective stack non mantiene la profondità di recupero")
    stack = complete_current(stack)
    if current_objective(stack) != "math.numbers.ratios":
        errors.append("objective stack non ritorna al recupero sospeso")
    stack = complete_current(stack)
    if current_objective(stack) != "math.numbers.proportions":
        errors.append("objective stack non ritorna al target originario")

    try:
        stack = push_recovery(stack, "a", reason="test", max_depth=2)
        stack = push_recovery(stack, "b", reason="test", max_depth=2)
        push_recovery(stack, "c", reason="test", max_depth=2)
        errors.append("objective stack consente una profondità oltre il limite")
    except ValueError:
        pass

    if errors:
        print("Adaptive engine validation: FAILED")
        for error in errors:
            print("-", error)
        return 1

    print("Adaptive engine validation: OK")
    print(f"Routing scenarios: {len(suite['scenarios'])}")
    print("Evidence pipeline: OK")
    print("Diagnostic planner: OK")
    print("Objective stack: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
