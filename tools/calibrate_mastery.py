#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from simulations.longitudinal import run_suite


def _raise_thresholds(values, delta):
    return {key: round(min(1.0, float(value) + delta), 3) for key, value in values.items()}


def _scale_advance(values, factor):
    result = dict(values)
    for key in ("accuracy", "independence", "stability", "transfer"):
        result[key] = round(float(result[key]) * factor, 3)
    return result


def candidates(current):
    conservative = deepcopy(current)
    conservative["strong_error_hypothesis"] = 0.72
    conservative["contradiction_threshold"] = 0.75
    conservative["recovery_exit"] = _raise_thresholds(conservative["recovery_exit"], 0.04)

    permissive = deepcopy(current)
    permissive["advance"] = _scale_advance(permissive["advance"], 0.95)

    strict_recovery = deepcopy(current)
    strict_recovery["recovery_exit"] = _raise_thresholds(strict_recovery["recovery_exit"], 0.08)

    return {
        "current_v0.2": current,
        "conservative": conservative,
        "permissive_advance": permissive,
        "strict_recovery_exit": strict_recovery,
    }


def score(metrics):
    return round(
        100
        - 220 * metrics["premature_advance_per_run"]
        - 80 * metrics["reassess_loop_per_run"]
        - 20 * metrics["false_recovery_per_run"]
        - 70 * (1 - metrics["recovery_detect_rate"])
        - 90 * (1 - metrics["recovery_return_rate"])
        - 55 * (1 - metrics["strong_progress_by_session_5"])
        - 90 * (1 - metrics["support_dependency_guard_rate"]),
        3,
    )


def main() -> int:
    current = json.loads((ROOT / "config" / "adaptive-policy.json").read_text(encoding="utf-8"))
    rows = []
    for name, policy in candidates(current).items():
        report = run_suite(policy, seeds=30, sessions=12)
        rows.append({"candidate": name, "score": score(report["metrics"]), "metrics": report["metrics"]})
    rows.sort(key=lambda row: row["score"], reverse=True)
    print(json.dumps({"synthetic_only": True, "ranking": rows}, indent=2, ensure_ascii=False))
    print("Calibration is advisory: this tool never rewrites policy files automatically.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
