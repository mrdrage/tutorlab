#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))

from engine.session_dispatch import dispatch

CASES=(
    ("math.us.algebra.factorisation",("scomponi",)),
    ("math.us.algebra.systems-linear",("sistema",)),
    ("math.us.data.conditional-probability-intro",("sapendo",)),
    ("math.us.functions.quadratic-functions",("zeri",)),
    ("math.us.scientifico.geometry.vectors",("modulo","u+v")),
    ("math.us.scientifico.probability.random-variables",("e[x]",)),
    ("eng.us.grammar.modals-b1",("modal","must","should","might")),
    ("eng.us.grammar.conditionals-b1",("if ",)),
    ("eng.us.grammar.complex-sentences-b1plus",("relative","although","because","so that")),
    ("eng.us.prof.vocabulary-work-b1plus",("professional","technical","colleague","customer","project")),
    ("eng.us.liceo.intercultural.b2-analysis",("stereotype","perspective","context")),
)


def prompts(competency_id):
    sent=dispatch(competency_id,"advance",competency_id,seed=31)
    if sent.get("status")!="ok": return None,sent
    texts=[task.get("prompt","").casefold() for phase in sent["session"].get("phases",[]) for task in phase.get("tasks",[])]
    return texts,sent


def main():
    errors=[]
    for cid,markers in CASES:
        texts,sent=prompts(cid)
        if texts is None:
            errors.append(f"{cid}: dispatch failed {sent}"); continue
        joined="\n".join(texts)
        if not any(marker.casefold() in joined for marker in markers):
            errors.append(f"{cid}: generated tasks do not expose expected competency markers {markers}")
    if errors:
        print("Upper Secondary generator alignment: FAILED")
        for error in errors: print("-",error)
        return 1
    print("Upper Secondary generator alignment: OK")
    print("Competency-specific samples checked:",len(CASES))
    return 0

if __name__=="__main__": raise SystemExit(main())
