from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = ROOT / "config" / "mastery-rubrics.json"


@lru_cache(maxsize=1)
def load_rubrics(path: str | None = None) -> dict[str, Any]:
    source = Path(path) if path else DEFAULT_CONFIG
    return json.loads(source.read_text(encoding="utf-8"))


def rubric_for(competency_id: str, config: dict[str, Any] | None = None) -> tuple[str, dict[str, Any]]:
    data = config or load_rubrics()
    for name, rubric in data.get("families", {}).items():
        if any(competency_id.startswith(prefix) for prefix in rubric.get("prefixes", [])):
            return name, rubric
    return "generic", data.get("default", {
        "min_independent_events": 2,
        "min_transfer_events": 1,
        "extend_transfer_events": 2,
        "priority_dimensions": [],
    })


def evidence_gate(
    competency_id: str,
    evidence_summary: dict[str, Any],
    *,
    for_extension: bool = False,
    config: dict[str, Any] | None = None,
) -> dict[str, Any]:
    family, rubric = rubric_for(competency_id, config)
    independent = int(evidence_summary.get("independent_event_count", 0))
    transfer = int(evidence_summary.get("transfer_event_count", 0))

    min_independent = int(rubric.get("min_independent_events", 0))
    transfer_key = "extend_transfer_events" if for_extension else "min_transfer_events"
    min_transfer = int(rubric.get(transfer_key, rubric.get("min_transfer_events", 0)))

    missing: list[str] = []
    if independent < min_independent:
        missing.append(f"independent_events:{independent}/{min_independent}")
    if transfer < min_transfer:
        missing.append(f"transfer_events:{transfer}/{min_transfer}")

    return {
        "family": family,
        "ready": not missing,
        "missing": missing,
        "priority_dimensions": list(rubric.get("priority_dimensions", [])),
    }
