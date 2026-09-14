#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from simulations.eight_year import run_suite_8y

CANDIDATE_WINDOWS = (0, 12, 18, 24)


def score(metrics: dict) -> float:
    return round(
        120 * metrics["premature_advance_per_run"]
        + 80 * metrics["false_recovery_per_run"]
        + 60 * metrics["reassess_loop_per_run"]
        + 80 * (1 - metrics["cross_stage_return_rate"])
        + 70 * (1 - metrics["deep_recovery_return_rate"])
        + 60 * (1 - metrics["cross_stage_complete_8y_rate"])
        + 50 * (1 - metrics["typical_complete_8y_rate"])
        + 35 * (1 - metrics["support_dependency_guard_rate"]),
        4,
    )


def main() -> int:
    baseline = json.loads((ROOT / "config" / "adaptive-policy.json").read_text(encoding="utf-8"))
    rows = []
    for window in CANDIDATE_WINDOWS:
        candidate = copy.deepcopy(baseline)
        if window:
            candidate["mastery_evidence_window"] = window
        else:
            candidate.pop("mastery_evidence_window", None)
        report = run_suite_8y(candidate, seeds=40, max_sessions_per_stage=16)
        rows.append({
            "mastery_evidence_window": window,
            "score": score(report["metrics"]),
            "metrics": report["metrics"],
        })

    rows.sort(key=lambda row: row["score"])
    print(json.dumps({"synthetic_only": True, "ranking": rows}, indent=2, ensure_ascii=False))
    configured = int(baseline.get("mastery_evidence_window", 0) or 0)
    best = rows[0]["mastery_evidence_window"]
    if configured != best:
        print(f"Calibration comparison: FAILED (configured={configured}, best={best})")
        return 1
    print(f"Calibration comparison: OK (configured window {configured} is best among {CANDIDATE_WINDOWS})")
    print("The script never edits production policy automatically.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
