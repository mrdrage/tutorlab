from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SECURE = {"secure", "extended"}
WEAK = {"emerging", "developing"}
PRIORITY = {"gateway": 0, "core": 1, "supporting": 2, "extension": 3}
SUPPORTED_SUBJECTS = {"mathematics", "english", "italian", "french", "spanish"}


def _folder(subject):
    if subject in SUPPORTED_SUBJECTS:
        return subject
    raise ValueError("unsupported subject")


def curriculum_nodes(subject, max_year=3):
    base = ROOT / "curriculum" / "middle-school" / _folder(subject)
    rows=[]
    for year in range(1, max_year + 1):
        data=json.loads((base / f"year-{year}.json").read_text(encoding="utf-8"))
        for order,node in enumerate(data.get("nodes", [])):
            item=dict(node); item["_order"]=order; rows.append(item)
    return rows


def _state(snapshot, subject, competency_id):
    return snapshot["subjects"][subject].get("competency_states", {}).get(competency_id)


def _status(state):
    return str((state or {}).get("status", "unknown"))


def _confidence(state):
    return float((state or {}).get("confidence", 0.0))


def _gate(node, snapshot, subject):
    for prerequisite in node.get("prerequisites", []):
        state=_state(snapshot,subject,prerequisite)
        if _status(state) in WEAK and _confidence(state) >= 0.55:
            return prerequisite,"known_prerequisite_gap"
    for prerequisite in node.get("prerequisites", []):
        state=_state(snapshot,subject,prerequisite)
        if _status(state)=="unknown" or _confidence(state)<0.35:
            return prerequisite,"prerequisite_needs_evidence"
    return None,None


def select_target(snapshot, subject, requested_target_id=None):
    subject_state=snapshot["subjects"][subject]
    stack=subject_state.get("objective_stack")
    if stack and stack.get("frames"):
        return {"root_target_id":stack["root_target_id"],"working_target_id":stack["frames"][-1]["competency_id"],"reason":"resume_objective_stack"}

    year=int(subject_state["typical_year"])
    nodes=curriculum_nodes(subject,year)
    index={node["id"]:node for node in nodes}

    if requested_target_id:
        if requested_target_id not in index: raise ValueError("requested target outside curriculum window")
        gate,reason=_gate(index[requested_target_id],snapshot,subject)
        if gate: return {"root_target_id":requested_target_id,"working_target_id":gate,"reason":reason}
        return {"root_target_id":requested_target_id,"working_target_id":requested_target_id,"reason":"explicit_target"}

    ordered=sorted(nodes,key=lambda n:(int(n.get("typical_year",1)),PRIORITY.get(n.get("priority"),9),n["_order"]))
    for node in ordered:
        state=_state(snapshot,subject,node["id"])
        if _status(state) in SECURE and _confidence(state)>=0.55: continue
        gate,reason=_gate(node,snapshot,subject)
        if gate: return {"root_target_id":node["id"],"working_target_id":gate,"reason":reason}
        return {"root_target_id":node["id"],"working_target_id":node["id"],"reason":"curriculum_frontier"}

    final=ordered[-1]
    return {"root_target_id":final["id"],"working_target_id":final["id"],"reason":"curriculum_mastered_extend"}


def suggested_successor(snapshot, subject, competency_id):
    year=int(snapshot["subjects"][subject]["typical_year"])
    for node in curriculum_nodes(subject,year):
        if competency_id in node.get("prerequisites",[]): return node["id"]
    return None
