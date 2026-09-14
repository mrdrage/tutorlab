#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CHECKS = (
    "tools/validate_curriculum.py",
    "tools/check_english_curriculum.py",
    "tools/check_adaptive_engine.py",
    "tools/check_session_engine.py",
    "tools/check_learning_snapshot.py",
    "tools/check_year1_generation_coverage.py",
    "tools/check_year2_generation_coverage.py",
    "tools/check_year3_generation_coverage.py",
    "tools/check_full_triennium_generation_coverage.py",
    "tools/check_language_expansion.py",
    "tools/run_longitudinal_simulations.py",
    "tools/check_upper_secondary_schemas.py",
    "tools/check_upper_secondary_architecture.py",
    "tools/check_upper_secondary_legacy_compat.py",
    "tools/check_upper_secondary_capability_boundary.py",
    "tools/check_cross_stage_recovery_bridge.py",
    "tools/check_upper_secondary_generation_coverage.py",
    "tools/check_upper_secondary_generation_quality.py",
    "tools/check_upper_secondary_vertical_slices.py",
)


def main() -> int:
    for relative in CHECKS:
        print(f"\n=== {relative} ===", flush=True)
        completed = subprocess.run([sys.executable, str(ROOT / relative)], cwd=ROOT, check=False)
        if completed.returncode != 0:
            print(f"Local validation stopped: {relative} failed.")
            return completed.returncode
    print("\nTutorLab local validation: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
