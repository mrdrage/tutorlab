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


def curriculum_ids(subject):
    path=ROOT/"curriculum"/"middle-school"/subject/"year-1.json"
    data=json.loads(path.read_text(encoding="utf-8"))
    return [node["id"] for node in data["nodes"]]


def check_task(task):
    errors=[]
    required={"task_id","family_id","prompt","response_mode","challenge_band","support_level","solution","rubric","evidence_dimensions","generation_parameters","fingerprint","competency_id"}
    missing=required-set(task)
    if missing: errors.append(f"missing task fields: {sorted(missing)}")
    if not task.get("prompt"): errors.append("empty prompt")
    if not task.get("rubric"): errors.append("missing rubric")
    if task.get("response_mode")=="open_response" and not task.get("solution"):
        errors.append("open response lacks tutor-side scoring target")
    return errors


def main():
    policy=load_policy(); registry=supported_competencies(); failures=[]; totals={}
    for subject in ("mathematics","english"):
        ids=curriculum_ids(subject); totals[subject]=len(ids)
        missing=sorted(set(ids)-registry)
        extra=sorted(x for x in registry if x.startswith("math." if subject=="mathematics" else "eng.") and x not in set(ids))
        if missing: failures.append(f"{subject}: uncovered nodes: {missing}")
        # Extra nodes are allowed because later years may become executable before this checker expands.
        for index,cid in enumerate(ids,1):
            for action,seed in (("advance",1000+index),("reassess",5000+index)):
                try:
                    session=build_session(cid,action,seed=seed,challenge_band=2,policy=policy)
                except Exception as exc:
                    failures.append(f"{cid}/{action}: build failed: {exc}")
                    continue
                quality=validate_session(session,policy)
                if quality: failures.append(f"{cid}/{action}: quality errors: {quality}")
                task_count=0
                for phase in session.get("phases",[]):
                    for task in phase.get("tasks",[]):
                        task_count+=1
                        for err in check_task(task): failures.append(f"{cid}/{action}/{task.get('task_id')}: {err}")
                if task_count==0: failures.append(f"{cid}/{action}: no tasks generated")
                view=student_view(session)
                leaked=[]
                for phase in view.get("phases",[]):
                    for task in phase.get("tasks",[]):
                        leaked.extend(key for key in ("solution","rubric","generation_parameters","error_signals") if key in task)
                if leaked: failures.append(f"{cid}/{action}: student view leaks {sorted(set(leaked))}")
    if failures:
        print("Year-1 generation coverage: FAILED")
        for failure in failures: print("-",failure)
        raise SystemExit(1)
    print("Year-1 generation coverage: OK")
    print(f"Mathematics nodes: {totals['mathematics']}")
    print(f"English nodes: {totals['english']}")
    print(f"Total executable year-1 nodes: {totals['mathematics']+totals['english']}")


if __name__=="__main__": main()
