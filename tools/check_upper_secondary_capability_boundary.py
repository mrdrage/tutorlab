#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from engine.session_dispatch import dispatch


def main():
    errors = []

    for competency_id in (
        "math.us.gateway.algebra-control",
        "math.us.gateway.representations-modelling",
        "eng.us.gateway.a2-integrated-control",
        "eng.us.gateway.a2-autonomy",
    ):
        result = dispatch(competency_id, "reassess", competency_id, seed=7)
        if result.get("status") != "needs_review":
            errors.append(f"{competency_id}: upper-secondary generation activated before v0.8")

    legacy = dispatch("math.numbers.signed-number-sense", "reassess", "math.numbers.signed-number-sense", seed=7)
    if legacy.get("status") != "ok":
        errors.append("existing middle-school generation capability regressed")

    if errors:
        print("Upper Secondary capability boundary: FAILED")
        for error in errors:
            print("-", error)
        return 1

    print("Upper Secondary capability boundary: OK")
    print("Upper gateway generation: needs_review")
    print("Middle-school generation: preserved")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
