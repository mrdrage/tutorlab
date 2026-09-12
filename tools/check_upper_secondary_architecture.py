#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from engine.academic_context import context_for, validate_context_shape
from engine.upper_secondary_resolver import curriculum_nodes, get_profile, load_catalog, validate_context
from engine.path_selector import select_target
from examples.learning_snapshot.synthetic_cases import mathematics_case, english_case


def middle_ids(subject):
    base = ROOT / "curriculum" / "middle-school" / subject
    result = set()
    for year in (1, 2, 3):
        data = json.loads((base / f"year-{year}.json").read_text(encoding="utf-8"))
        result.update(node["id"] for node in data.get("nodes", []))
    return result


def upper_ids(subject):
    base = ROOT / "curriculum" / "upper-secondary" / subject
    result = set()
    for path in base.rglob("*.json"):
        data = json.loads(path.read_text(encoding="utf-8"))
        result.update(node["id"] for node in data.get("nodes", []))
    return result


def main():
    errors = []
    if (ROOT / ".github" / "workflows").exists():
        errors.append("GitHub workflows directory must remain absent")

    catalog = load_catalog()
    profiles = catalog.get("profiles", [])
    profile_ids = [item.get("id") for item in profiles]
    if len(profile_ids) != len(set(profile_ids)):
        errors.append("duplicate pathway profile ids")
    source_ids = {item.get("id") for item in catalog.get("sources", [])}
    for profile in profiles:
        unknown = set(profile.get("source_refs", [])) - source_ids
        if unknown:
            errors.append(f"{profile['id']}: unknown source refs {sorted(unknown)}")
    if {item.get("family") for item in profiles} != {"liceo", "tecnico", "professionale"}:
        errors.append("seed catalog must cover liceo, tecnico and professionale")
    if not any(item.get("duration_years") == 4 for item in profiles):
        errors.append("seed catalog must include a four-year pathway")
    if not any(item.get("duration_years") == 5 for item in profiles):
        errors.append("seed catalog must include a five-year pathway")

    legacy_math = mathematics_case()
    legacy_eng = english_case()
    if context_for(legacy_math, "mathematics")["school_stage"] != "middle_school":
        errors.append("legacy math snapshot no longer defaults to middle school")
    if context_for(legacy_eng, "english")["stage_year"] != int(legacy_eng["subjects"]["english"]["typical_year"]):
        errors.append("legacy English typical_year compatibility broken")

    contexts = {
        "scientifico": {
            "school_stage": "upper_secondary", "stage_year": 1, "school_year": "2026/27",
            "pathway_profile_id": "it.upper.liceo-scientifico", "pathway_variant": "standard",
            "curriculum_profile_ids": []
        },
        "informatica": {
            "school_stage": "upper_secondary", "stage_year": 1, "school_year": "2026/27",
            "pathway_profile_id": "it.upper.tecnico-informatica", "pathway_variant": "standard",
            "curriculum_profile_ids": []
        },
        "professionale": {
            "school_stage": "upper_secondary", "stage_year": 1, "school_year": "2026/27",
            "pathway_profile_id": "it.upper.professionale-manutenzione", "pathway_variant": "standard",
            "curriculum_profile_ids": []
        },
        "quadriennale": {
            "school_stage": "upper_secondary", "stage_year": 4, "school_year": "2026/27",
            "pathway_profile_id": "it.upper.tecnico-informatica-4y", "pathway_variant": "quadriennale_filiera",
            "curriculum_profile_ids": []
        }
    }
    for label, context in contexts.items():
        if validate_context_shape(context):
            errors.append(f"{label}: invalid academic context shape")
        if validate_context(context):
            errors.append(f"{label}: invalid pathway context")

    invalid_5y = dict(contexts["quadriennale"], stage_year=5)
    if "stage_year_exceeds_pathway_duration" not in validate_context(invalid_5y):
        errors.append("four-year pathway accepted stage year 5")
    mismatch = dict(contexts["informatica"], pathway_variant="quadriennale_filiera")
    if "pathway_variant_mismatch" not in validate_context(mismatch):
        errors.append("pathway variant mismatch not detected")

    sci_math = {node["id"] for node in curriculum_nodes("mathematics", contexts["scientifico"])}
    tech_math = {node["id"] for node in curriculum_nodes("mathematics", contexts["informatica"])}
    prof_math = {node["id"] for node in curriculum_nodes("mathematics", contexts["professionale"])}
    common = {"math.us.gateway.algebra-control", "math.us.gateway.representations-modelling"}
    if not common.issubset(sci_math & tech_math & prof_math):
        errors.append("common math gateway not shared across pathway families")
    if "math.us.gateway.scientific-reasoning" not in sci_math or "math.us.gateway.scientific-reasoning" in tech_math:
        errors.append("scientific profile overlay composition failed")
    if "math.us.gateway.technical-modelling" not in tech_math or "math.us.gateway.technical-modelling" in sci_math:
        errors.append("technical family overlay composition failed")
    if {"math.us.gateway.scientific-reasoning", "math.us.gateway.technical-modelling"} & prof_math:
        errors.append("professional profile received unrelated math overlay")

    for context in contexts.values():
        eng = {node["id"] for node in curriculum_nodes("english", context)}
        if not {"eng.us.gateway.a2-integrated-control", "eng.us.gateway.a2-autonomy"}.issubset(eng):
            errors.append("common English gateway not available to a valid profile")

    all_known = middle_ids("mathematics") | middle_ids("english") | upper_ids("mathematics") | upper_ids("english")
    for subject in ("mathematics", "english"):
        base = ROOT / "curriculum" / "upper-secondary" / subject
        for path in base.rglob("*.json"):
            data = json.loads(path.read_text(encoding="utf-8"))
            for node in data.get("nodes", []):
                missing = set(node.get("prerequisites", [])) - all_known
                if missing:
                    errors.append(f"{node['id']}: unresolved prerequisites {sorted(missing)}")

    upper_snapshot = mathematics_case()
    upper_snapshot["version"] = "0.2"
    upper_snapshot["academic_context"] = contexts["scientifico"]
    upper_snapshot["subjects"]["mathematics"]["typical_year"] = 1
    selection = select_target(upper_snapshot, "mathematics", "math.us.gateway.algebra-control")
    if selection.get("root_target_id") != "math.us.gateway.algebra-control":
        errors.append("upper-secondary target selector did not use resolved graph")
    if selection.get("working_target_id") not in set(get_profile(contexts["scientifico"]["pathway_profile_id"]) and [
        "math.us.gateway.algebra-control",
        "math.numbers.signed-operations",
        "math.relations.algebraic-expressions",
        "math.relations.first-degree-equations"
    ]):
        errors.append("upper-secondary target selector returned unexpected target")

    if errors:
        print("Upper Secondary Architecture validation: FAILED")
        for error in errors:
            print("-", error)
        return 1

    print("Upper Secondary Architecture validation: OK")
    print("Profiles in seed catalog:", len(profiles))
    print("Scientific math nodes:", len(sci_math))
    print("Technical math nodes:", len(tech_math))
    print("Professional math nodes:", len(prof_math))
    print("Legacy middle-school context: preserved")
    print("GitHub Actions/workflows: absent")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
