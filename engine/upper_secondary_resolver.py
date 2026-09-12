from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "curriculum" / "upper-secondary" / "pathways" / "catalog.seed.json"


def load_catalog():
    return json.loads(CATALOG.read_text(encoding="utf-8"))


def get_profile(profile_id):
    for profile in load_catalog().get("profiles", []):
        if profile.get("id") == profile_id:
            return profile
    raise ValueError(f"unknown pathway profile: {profile_id}")


def validate_context(context):
    try:
        profile = get_profile(context.get("pathway_profile_id"))
    except ValueError:
        return ["unknown_pathway_profile"]
    errors = []
    year = int(context.get("stage_year", 0) or 0)
    if not 1 <= year <= int(profile["duration_years"]):
        errors.append("stage_year_exceeds_pathway_duration")
    if context.get("pathway_variant") != profile.get("pathway_variant"):
        errors.append("pathway_variant_mismatch")
    return errors


def _layer_matches(layer, profile):
    kind = layer.get("kind")
    if kind == "common_core":
        return True
    if kind == "family_core":
        return layer.get("family") == profile.get("family")
    return profile.get("id") in set(layer.get("profile_ids") or [])


def _node_matches(node, profile):
    profile_id = profile.get("id")
    included = set(node.get("applies_to_profile_ids") or [])
    excluded = set(node.get("excludes_profile_ids") or [])
    return profile_id not in excluded and (not included or profile_id in included)


def graph_files(subject):
    base = ROOT / "curriculum" / "upper-secondary" / subject
    return sorted(base.rglob("*.json")) if base.exists() else []


def curriculum_nodes(subject, context):
    errors = validate_context(context)
    if errors:
        raise ValueError(",".join(errors))
    profile = get_profile(context["pathway_profile_id"])
    max_year = int(context["stage_year"])
    result, seen = [], set()
    for path in graph_files(subject):
        graph = json.loads(path.read_text(encoding="utf-8"))
        if not _layer_matches(graph.get("layer", {}), profile):
            continue
        for order, node in enumerate(graph.get("nodes", [])):
            if int(node.get("stage_year", 0)) > max_year or not _node_matches(node, profile):
                continue
            if node["id"] in seen:
                raise ValueError(f"duplicate composed competency: {node['id']}")
            item = dict(node)
            item["_order"] = order
            item["_layer"] = graph["layer"]["kind"]
            item["_curriculum_profile"] = graph["curriculum_profile"]
            result.append(item)
            seen.add(node["id"])
    return result


def curriculum_profiles(subject, context):
    profile = get_profile(context["pathway_profile_id"])
    rows = []
    for path in graph_files(subject):
        graph = json.loads(path.read_text(encoding="utf-8"))
        if _layer_matches(graph.get("layer", {}), profile):
            rows.append(graph["curriculum_profile"])
    return rows
