#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))

from engine.session_engine import build_session, load_policy
from engine.session_quality import validate_session
from engine.task_families import supported_competencies

ACTIONS=("recover","consolidate","advance","extend","reassess")


def curriculum_ids(subject,year):
    data=json.loads((ROOT/"curriculum"/"middle-school"/subject/f"year-{year}.json").read_text(encoding="utf-8"))
    return [node["id"] for node in data["nodes"]]


def main():
    policy=load_policy(); registry=supported_competencies(); failures=[]; counts={}; variants=0; all_ids=[]
    for year in (1,2,3):
        for subject in ("mathematics","english"):
            ids=curriculum_ids(subject,year); counts[(year,subject)]=len(ids); all_ids.extend(ids)
            missing=sorted(set(ids)-registry)
            if missing: failures.append(f"year {year} {subject}: uncovered {missing}")
            for index,cid in enumerate(ids,1):
                for offset,action in enumerate(ACTIONS,1):
                    variants+=1
                    try:
                        session=build_session(cid,action,seed=30000+year*1000+index*10+offset,challenge_band=min(4,year+1),policy=policy)
                    except Exception as exc:
                        failures.append(f"{cid}/{action}: build failed: {exc}"); continue
                    quality=validate_session(session,policy)
                    if quality: failures.append(f"{cid}/{action}: {quality}")
    if len(all_ids)!=len(set(all_ids)):
        failures.append("duplicate competency id appears across yearly curriculum files")
    if failures:
        print("Full triennium generation coverage: FAILED")
        for failure in failures: print("-",failure)
        return 1
    total=len(all_ids)
    print("Full triennium generation coverage: OK")
    for year in (1,2,3):
        print(f"Year {year}: Math {counts[(year,'mathematics')]}, English {counts[(year,'english')]}.")
    print(f"Total curriculum nodes executable: {total}")
    print(f"Adaptive session variants exercised: {variants}")
    return 0


if __name__=="__main__": raise SystemExit(main())
