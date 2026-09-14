#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from simulations.eight_year import run_suite_8y


def main() -> int:
    policy = json.loads((ROOT / "config" / "adaptive-policy.json").read_text(encoding="utf-8"))
    report = run_suite_8y(policy, seeds=100, max_sessions_per_stage=16)
    print(json.dumps(report, indent=2, ensure_ascii=False))

    metrics = report["metrics"]
    checks = {
        "premature advancement stays rare": metrics["premature_advance_per_run"] <= 0.02,
        "false recovery stays rare": metrics["false_recovery_per_run"] <= 0.02,
        "reassessment loops stay rare": metrics["reassess_loop_per_run"] <= 0.02,
        "strong profiles complete eight stages": metrics["strong_complete_8y_rate"] >= 0.98,
        "typical profiles complete eight stages": metrics["typical_complete_8y_rate"] >= 0.95,
        "cross-stage gap profiles usually complete eight stages": metrics["cross_stage_complete_8y_rate"] >= 0.85,
        "cross-stage gaps are detected": metrics["cross_stage_recovery_detect_rate"] >= 0.95,
        "cross-stage recoveries return to the suspended target": metrics["cross_stage_return_rate"] >= 0.95,
        "nested recoveries are detected": metrics["deep_recovery_detect_rate"] >= 0.85,
        "nested recoveries return in stack order": metrics["deep_recovery_return_rate"] >= 0.85,
        "support-dependent profiles are protected from early advancement": metrics["support_dependency_guard_rate"] >= 0.98,
    }
    failed = [name for name, ok in checks.items() if not ok]
    if failed:
        print("Eight-year longitudinal reliability: FAILED")
        for name in failed:
            print("-", name)
        return 1
    print("Eight-year longitudinal reliability: OK")
    print("Synthetic engineering validation only; not a validation on real students.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
