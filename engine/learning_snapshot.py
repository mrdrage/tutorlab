from __future__ import annotations

from copy import deepcopy


def competency_state(snapshot, subject, competency_id):
    return snapshot["subjects"][subject].get("competency_states", {}).get(competency_id, {
        "competency_id": competency_id,
        "status": "unknown",
        "confidence": 0.0,
        "mastery": {},
        "evidence_summary": {"independent_event_count": 0, "contradiction_level": 0.0},
        "error_hypotheses": [],
    })


def with_objective_stack(snapshot, subject, stack):
    updated = deepcopy(snapshot)
    updated["subjects"][subject]["objective_stack"] = stack
    return updated


def with_recent_activity(snapshot, session):
    updated = deepcopy(snapshot)
    recent = updated.setdefault("recent_activity", {"session_ids": [], "fingerprints": []})
    ids = list(recent.get("session_ids", []))
    if session["session_id"] not in ids:
        ids.append(session["session_id"])
    recent["session_ids"] = ids[-50:]
    prints = list(recent.get("fingerprints", []))
    for phase in session.get("phases", []):
        for task in phase.get("tasks", []):
            fp = task.get("fingerprint")
            if fp and fp not in prints:
                prints.append(fp)
    recent["fingerprints"] = prints[-500:]
    return updated
