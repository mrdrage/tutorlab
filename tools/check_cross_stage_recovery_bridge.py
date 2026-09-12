#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from engine.path_selector import select_target
from engine.session_dispatch import dispatch
from engine.stack_bridge import ensure_stack
from examples.learning_snapshot.synthetic_cases import mathematics_case

POLICY = json.loads((ROOT / "config" / "adaptive-policy.json").read_text(encoding="utf-8"))


def main():
    errors = []
    snapshot = mathematics_case()
    snapshot["version"] = "0.2"
    snapshot["academic_context"] = {
        "school_stage": "upper_secondary",
        "stage_year": 1,
        "school_year": "2026/27",
        "pathway_profile_id": "it.upper.liceo-scientifico",
        "pathway_variant": "standard",
        "curriculum_profile_ids": ["it-upper-math-gateway-2026"]
    }

    root = "math.us.gateway.algebra-control"
    selection = select_target(snapshot, "mathematics", root)
    if selection.get("root_target_id") != root:
        errors.append(f"wrong root target: {selection}")
    working = selection.get("working_target_id")
    if working != "math.numbers.signed-operations":
        errors.append(f"expected first cross-stage prerequisite, got {working}")

    stack = ensure_stack(None, selection, int(POLICY["max_recovery_depth"]))
    frames = stack.get("frames", [])
    if len(frames) != 2 or frames[0].get("competency_id") != root or frames[-1].get("competency_id") != working:
        errors.append(f"cross-stage objective stack malformed: {stack}")

    if working:
        sent = dispatch(working, "reassess", root, seed=17)
        if sent.get("status") != "ok":
            errors.append(f"middle-school prerequisite is not executable: {sent}")
        else:
            session = sent["session"]
            if session.get("target_competency_id") != working:
                errors.append("session target does not match recovered prerequisite")
            if session.get("original_target_id") != root:
                errors.append("session lost suspended upper-secondary root target")

    if errors:
        print("Cross-stage recovery bridge: FAILED")
        for error in errors:
            print("-", error)
        return 1

    print("Cross-stage recovery bridge: OK")
    print("Upper root:", root)
    print("Recovered lower prerequisite:", working)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
