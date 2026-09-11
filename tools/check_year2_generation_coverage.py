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


def curriculum_ids(subject):
    data=json.loads((ROOT/"curriculum"/"middle-school"/subject/"year-2.json").read_text(encoding="utf-8"))
    return [node["id"] for node in data["nodes"]]


def check_task(task):
    required={"task_id","family_id","prompt","response_mode","challenge_band","support_level","solution","rubric","evidence_dimensions","generation_parameters","fingerprint","competency_id"}
    errors=[]
    missing=required-set(task)
    if missing: errors.append(f"missing task fields: {sorted(missing)}")
    if not task.get("prompt"): errors.append("empty prompt")
    if not task.get("rubric"): errors.append("missing rubric")
    if task.get("response_mode")=="open_response" and not task.get("solution"):
        errors.append("open response lacks tutor-side scoring target")
    return errors


def main():
    policy=load_policy(); registry=supported_competencies(); failures=[]; totals={}; variants=0
    for subject in ("mathematics","english"):
        ids=curriculum_ids(subject); totals[subject]=len(ids)
        missing=sorted(set(ids)-registry)
        if missing: failures.append(f"{subject}: uncovered nodes: {missing}")
        for index,cid in enumerate(ids,1):
            for offset,action in enumerate(ACTIONS,1):
                variants+=1
                try:
                    session=build_session(cid,action,seed=10000+index*10+offset,challenge_band=2,policy=policy)
                except Exception as exc:
                    failures.append(f"{cid}/{action}: build failed: {exc}")
                    continue
                quality=validate_session(session,policy)
                if quality: failures.append(f"{cid}/{action}: quality errors: {quality}")
                count=0
                for phase in session.get("phases",[]):
                    for item in phase.get("tasks",[]):
                        count+=1
                        for err in check_task(item): failures.append(f"{cid}/{action}/{item.get('task_id')}: {err}")
                if count==0: failures.append(f"{cid}/{action}: no tasks generated")
                view=student_view(session)
                leaked=[]
                for phase in view.get("phases",[]):
                    for item in phase.get("tasks",[]):
                        leaked.extend(key for key in ("solution","rubric","generation_parameters","error_signals") if key in item)
                if leaked: failures.append(f"{cid}/{action}: student view leaks {sorted(set(leaked))}")
    if failures:
        print("Year-2 generation coverage: FAILED")
        for failure in failures: print("-",failure)
        return 1
    print("Year-2 generation coverage: OK")
    print(f"Mathematics nodes: {totals['mathematics']}")
    print(f"English nodes: {totals['english']}")
    print(f"Total executable year-2 nodes: {totals['mathematics']+totals['english']}")
    print(f"Adaptive session variants exercised: {variants}")
    return 0


if __name__=="__main__": raise SystemExit(main())
