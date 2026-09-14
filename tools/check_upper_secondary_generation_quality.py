#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))

from engine.session_engine import build_session,load_policy,student_view
from engine.session_quality import validate_session

SEEDS=(17,31,47,59,73,89)


def all_nodes():
    out={}
    for subject in ("mathematics","english"):
        rows={}
        for path in sorted((ROOT/"curriculum"/"upper-secondary"/subject).rglob("*.json")):
            data=json.loads(path.read_text(encoding="utf-8"))
            for node in data.get("nodes",[]): rows[node["id"]]=node
        out[subject]=rows
    return out


def tasks_for(session,kind):
    return [t for p in session.get("phases",[]) if p.get("kind")==kind for t in p.get("tasks",[])]


def main():
    policy=load_policy(); failures=[]; nodes=all_nodes(); samples=[]
    for subject,index in nodes.items():
        by=defaultdict(list)
        for node in index.values(): by[node.get("strand","unknown")].append(node)
        for strand,rows in sorted(by.items()):
            rows.sort(key=lambda n:(int(n.get("stage_year",1)),n["id"]))
            samples.append((subject,strand,rows[-1]))

    for subject,strand,node in samples:
        cid=node["id"]; semantic_variants=set()
        for seed in SEEDS:
            try: session=build_session(cid,"advance",original_target_id=cid,seed=seed,policy=policy)
            except Exception as exc:
                failures.append(f"{cid}: build failed: {exc}"); continue
            quality=validate_session(session,policy)
            if quality: failures.append(f"{cid}: quality {quality}"); continue
            model=tasks_for(session,"worked_example")
            if not model: failures.append(f"{cid}: no worked example task")
            else:
                text=model[0].get("prompt","").lower()
                if not any(marker in text for marker in ("esempio svolto","worked example","model")):
                    failures.append(f"{cid}: worked example is not visibly modelled")
            transfer=tasks_for(session,"transfer")
            if not transfer: failures.append(f"{cid}: no transfer task")
            else:
                item=transfer[0]
                payload=item.get("prompt","")
                if subject=="english" and strand=="listening":
                    payload=item.get("generation_parameters",{}).get("tutor_script",payload)
                semantic_variants.add(payload)
                if item.get("response_mode")=="open_response" and not item.get("rubric"):
                    failures.append(f"{cid}: open transfer task lacks rubric")
            if subject=="english" and strand=="listening":
                all_tasks=[t for p in session.get("phases",[]) for t in p.get("tasks",[])]
                if not any(t.get("generation_parameters",{}).get("tutor_script") for t in all_tasks):
                    failures.append(f"{cid}: listening task lacks tutor script")
                sv=student_view(session)
                if any("generation_parameters" in t for p in sv["phases"] for t in p.get("tasks",[])):
                    failures.append(f"{cid}: tutor data leaked to student view")
        if len(semantic_variants)<2: failures.append(f"{cid}: insufficient semantic diversity across seeds")

    if failures:
        print("Upper Secondary generation quality: FAILED")
        for failure in failures: print("-",failure)
        return 1
    print("Upper Secondary generation quality: OK")
    print("Representative strands checked:",len(samples))
    print("Seeds per strand:",len(SEEDS))
    return 0

if __name__=="__main__": raise SystemExit(main())
