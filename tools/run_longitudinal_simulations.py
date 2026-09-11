#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from simulations.longitudinal import run_suite


def main() -> int:
    policy = json.loads((ROOT / "config" / "adaptive-policy.json").read_text(encoding="utf-8"))
    report = run_suite(policy, seeds=50, sessions=12)
    print(json.dumps(report, indent=2, ensure_ascii=False))

    metrics = report["metrics"]
    checks = {
        "no systematic premature advancement": metrics["premature_advance_per_run"] <= 0.02,
        "no reassessment loops": metrics["reassess_loop_per_run"] <= 0.02,
        "prerequisite gaps detected": metrics["recovery_detect_rate"] >= 0.90,
        "recovery returns to suspended target": metrics["recovery_return_rate"] >= 0.90,
        "strong profiles can progress": metrics["strong_progress_by_session_5"] >= 0.95,
        "support-dependent profiles do not advance early": metrics["support_dependency_guard_rate"] >= 0.95,
    }
    failed = [name for name, ok in checks.items() if not ok]
    if failed:
        print("Longitudinal simulation acceptance: FAILED")
        for name in failed:
            print("-", name)
        return 1
    print("Longitudinal simulation acceptance: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
