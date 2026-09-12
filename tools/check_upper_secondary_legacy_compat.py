#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from engine.objective_stack import start_objective
from engine.path_selector import select_target
from examples.learning_snapshot.synthetic_cases import english_case, mathematics_case


def main():
    errors = []

    math = mathematics_case()
    selected = select_target(math, "mathematics", "math.numbers.fraction-equivalence")
    expected = {
        "root_target_id": "math.numbers.fraction-equivalence",
        "working_target_id": "math.numbers.fraction-equivalence",
        "reason": "explicit_target",
    }
    if selected != expected:
        errors.append(f"legacy math explicit target changed: {selected}")

    eng = english_case()
    selected = select_target(eng, "english", "eng.grammar.present_simple")
    if selected.get("root_target_id") != "eng.grammar.present_simple":
        errors.append(f"legacy English root target changed: {selected}")
    if selected.get("working_target_id") not in {"eng.grammar.present_simple", "eng.grammar.be"}:
        errors.append(f"legacy English prerequisite behaviour changed: {selected}")

    resume = english_case()
    resume["subjects"]["english"]["objective_stack"] = start_objective("eng.grammar.present_simple")
    selected = select_target(resume, "english")
    if selected.get("reason") != "resume_objective_stack":
        errors.append("objective stack no longer has priority")

    if errors:
        print("Upper Secondary legacy compatibility: FAILED")
        for error in errors:
            print("-", error)
        return 1

    print("Upper Secondary legacy compatibility: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
