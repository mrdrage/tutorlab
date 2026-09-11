#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))

from engine.session_engine import build_session, load_policy, student_view
from engine.session_quality import validate_session
from engine.task_families import supported_competencies

ACTIONS=("recover","consolidate","advance","extend","reassess")


def ids(subject):
    data=json.loads((ROOT/"curriculum"/"middle-school"/subject/"year-3.json").read_text(encoding="utf-8"))
    return [node["id"] for node in data["nodes"]]


def main():
    policy=load_policy(); registry=supported_competencies(); failures=[]; totals={}; variants=0
    required={"task_id","family_id","prompt","response_mode","challenge_band","support_level","solution","rubric","evidence_dimensions","generation_parameters","fingerprint","competency_id"}
    for subject in ("mathematics","english"):
        nodes=ids(subject); totals[subject]=len(nodes)
        missing=sorted(set(nodes)-registry)
        if missing: failures.append(f"{subject}: uncovered nodes: {missing}")
        for index,cid in enumerate(nodes,1):
            for offset,action in enumerate(ACTIONS,1):
                variants+=1
                try:
                    session=build_session(cid,action,seed=20000+index*10+offset,challenge_band=3,policy=policy)
                except Exception as exc:
                    failures.append(f"{cid}/{action}: build failed: {exc}"); continue
                quality=validate_session(session,policy)
                if quality: failures.append(f"{cid}/{action}: quality errors: {quality}")
                task_count=0
                for phase in session.get("phases",[]):
                    for item in phase.get("tasks",[]):
                        task_count+=1
                        missing_fields=required-set(item)
                        if missing_fields: failures.append(f"{cid}/{action}: missing fields {sorted(missing_fields)}")
                        if not item.get("prompt"): failures.append(f"{cid}/{action}: empty prompt")
                        if not item.get("rubric"): failures.append(f"{cid}/{action}: missing rubric")
                if not task_count: failures.append(f"{cid}/{action}: no tasks generated")
                for phase in student_view(session).get("phases",[]):
                    for item in phase.get("tasks",[]):
                        leaked=[k for k in ("solution","rubric","generation_parameters","error_signals") if k in item]
                        if leaked: failures.append(f"{cid}/{action}: student view leaks {leaked}")
    if failures:
        print("Year-3 generation coverage: FAILED")
        for failure in failures: print("-",failure)
        return 1
    print("Year-3 generation coverage: OK")
    print(f"Mathematics nodes: {totals['mathematics']}")
    print(f"English nodes: {totals['english']}")
    print(f"Total executable year-3 nodes: {totals['mathematics']+totals['english']}")
    print(f"Adaptive session variants exercised: {variants}")
    return 0


if __name__=="__main__": raise SystemExit(main())
