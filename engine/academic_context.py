from __future__ import annotations

from copy import deepcopy
from typing import Any


def context_for(snapshot: dict[str, Any], subject: str) -> dict[str, Any]:
    """Return normalized academic context with backward compatibility.

    Legacy middle-school snapshots do not contain academic_context. They are interpreted
    exactly as before from subjects[subject].typical_year.
    """
    raw = snapshot.get("academic_context")
    if raw:
        return deepcopy(raw)
    year = int(snapshot["subjects"][subject]["typical_year"])
    return {
        "school_stage": "middle_school",
        "stage_year": year,
        "school_year": "2026/27",
        "pathway_profile_id": None,
        "pathway_variant": None,
        "curriculum_profile_ids": [],
    }


def validate_context_shape(context: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    stage = context.get("school_stage")
    year = int(context.get("stage_year", 0) or 0)
    if stage not in {"middle_school", "upper_secondary"}:
        errors.append("unsupported_school_stage")
        return errors
    max_year = 3 if stage == "middle_school" else 5
    if year < 1 or year > max_year:
        errors.append("stage_year_out_of_range")
    if stage == "middle_school":
        if context.get("pathway_profile_id") is not None:
            errors.append("middle_school_must_not_have_pathway_profile")
    else:
        if not context.get("pathway_profile_id"):
            errors.append("upper_secondary_requires_pathway_profile")
        if not context.get("pathway_variant"):
            errors.append("upper_secondary_requires_pathway_variant")
    return errors
