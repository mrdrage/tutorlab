#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))

from engine.session_dispatch import dispatch


def main():
    errors=[]
    supported=(
        "math.us.gateway.algebra-control",
        "math.us.algebra.linear-equations",
        "math.us.scientifico.calculus.optimization",
        "eng.us.gateway.a2-integrated-control",
        "eng.us.reading.b1-gist-detail",
        "eng.us.liceo.integrated.b2-target",
        "eng.us.prof.integrated-b1plus-target",
    )
    for competency_id in supported:
        result=dispatch(competency_id,"reassess",competency_id,seed=7)
        if result.get("status")!="ok":
            errors.append(f"{competency_id}: expected generation coverage, got {result}")

    legacy=dispatch("math.numbers.signed-number-sense","reassess","math.numbers.signed-number-sense",seed=7)
    if legacy.get("status")!="ok": errors.append("existing middle-school generation capability regressed")

    outside=("math.future.out-of-scope","eng.future.out-of-scope")
    for competency_id in outside:
        result=dispatch(competency_id,"reassess",competency_id,seed=7)
        if result.get("status")!="needs_review":
            errors.append(f"{competency_id}: out-of-scope boundary missing")

    if errors:
        print("Upper Secondary capability boundary: FAILED")
        for error in errors: print("-",error)
        return 1
    print("Upper Secondary capability boundary: OK")
    print("Upper Math/English generation: enabled")
    print("Middle-school generation: preserved")
    print("Unknown future nodes: needs_review")
    return 0

if __name__=="__main__": raise SystemExit(main())
