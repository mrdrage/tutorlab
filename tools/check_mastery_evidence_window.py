#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from engine.reliability_state import calibrated_state


def event(index: int, status: str) -> dict:
    return {
        "event_id": f"window-{index}",
        "competency_id": "math.us.algebra.linear-equations",
        "observed_at": f"2031-01-{index:02d}T10:00:00+01:00",
        "outcome": {
            "status": status,
            "transfer_success": 0.88 if status == "correct" else 0.15,
            "explanation_quality": 0.86 if status == "correct" else 0.25,
        },
        "support": {"level": "none"},
        "task": {"context_familiarity": "near_transfer"},
        "error_observations": [],
        "tags": [],
    }


def main() -> int:
    policy = json.loads((ROOT / "config" / "adaptive-policy.json").read_text(encoding="utf-8"))
    window = int(policy.get("mastery_evidence_window", 0) or 0)
    if window != 12:
        print(f"Mastery evidence window: FAILED (expected 12, got {window})")
        return 1

    events = [event(index, "incorrect") for index in range(1, 9)]
    events.extend(event(index, "correct") for index in range(9, 21))
    state = calibrated_state("math.us.algebra.linear-equations", events, policy)
    summary = state["evidence_summary"]
    failures = []
    if summary.get("lifetime_event_count") != 20:
        failures.append("lifetime history count was not preserved")
    if summary.get("active_window_event_count") != 12:
        failures.append("active mastery window is not 12 events")
    accuracy = state["mastery"]["accuracy"]
    value = float(accuracy.get("value", 0.0)) * float(accuracy.get("confidence", 0.0))
    if value < 0.90:
        failures.append(f"recent clean evidence did not dominate mastery as expected: {value}")

    if failures:
        print("Mastery evidence window: FAILED")
        for failure in failures:
            print("-", failure)
        return 1
    print("Mastery evidence window: OK")
    print("Lifetime evidence retained: 20")
    print("Active mastery evidence: 12 recent events")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
