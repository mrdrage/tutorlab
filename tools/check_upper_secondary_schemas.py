#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SCHEMA_FILES = (
    ROOT / "schemas" / "education-pathway.schema.json",
    ROOT / "schemas" / "academic-context.schema.json",
    ROOT / "schemas" / "upper-secondary-curriculum-graph.schema.json",
    ROOT / "schemas" / "learning-snapshot.schema.json",
)


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main():
    failures = []
    schemas = {}
    for path in SCHEMA_FILES:
        try:
            schemas[path.name] = load(path)
        except Exception as exc:
            failures.append(f"{path.name}: invalid JSON: {exc}")

    catalog_path = ROOT / "curriculum" / "upper-secondary" / "pathways" / "catalog.seed.json"
    graph_paths = sorted((ROOT / "curriculum" / "upper-secondary").glob("*/**/*.json"))
    graph_paths = [p for p in graph_paths if "pathways" not in p.parts]
    try:
        catalog = load(catalog_path)
    except Exception as exc:
        failures.append(f"catalog.seed.json: invalid JSON: {exc}")
        catalog = None

    graphs = []
    for path in graph_paths:
        try:
            graphs.append((path, load(path)))
        except Exception as exc:
            failures.append(f"{path.relative_to(ROOT)}: invalid JSON: {exc}")

    try:
        from jsonschema import Draft202012Validator
    except ImportError:
        Draft202012Validator = None

    if Draft202012Validator is not None and not failures:
        for name, schema in schemas.items():
            try:
                Draft202012Validator.check_schema(schema)
            except Exception as exc:
                failures.append(f"{name}: invalid Draft 2020-12 schema: {exc}")

        def require_valid(validator, payload, label):
            errors = list(validator.iter_errors(payload))
            if errors:
                failures.append(f"{label}: expected valid, got {errors[0].message}")

        def require_invalid(validator, payload, label):
            if not list(validator.iter_errors(payload)):
                failures.append(f"{label}: expected invalid but schema accepted it")

        if catalog is not None:
            pathway_validator = Draft202012Validator(schemas["education-pathway.schema.json"])
            require_valid(pathway_validator, catalog, "catalog.seed.json")

        graph_validator = Draft202012Validator(schemas["upper-secondary-curriculum-graph.schema.json"])
        for path, graph in graphs:
            require_valid(graph_validator, graph, str(path.relative_to(ROOT)))

        if graphs:
            family_without_family = copy.deepcopy(graphs[0][1])
            family_without_family["layer"] = {"kind":"family_core", "profile_ids":[]}
            require_invalid(graph_validator, family_without_family, "family_core without family")

            profile_without_ids = copy.deepcopy(graphs[0][1])
            profile_without_ids["layer"] = {"kind":"profile", "family":"liceo", "profile_ids":[]}
            require_invalid(graph_validator, profile_without_ids, "profile layer without profile_ids")

            bad_namespace = copy.deepcopy(graphs[0][1])
            bad_namespace["nodes"][0]["id"] = "math.gateway.invalid"
            require_invalid(graph_validator, bad_namespace, "upper graph node without .us namespace")

        context_validator = Draft202012Validator(schemas["academic-context.schema.json"])
        sample_contexts = (
            {"school_stage":"middle_school","stage_year":2,"school_year":"2026/27","pathway_profile_id":None,"pathway_variant":None,"curriculum_profile_ids":[]},
            {"school_stage":"upper_secondary","stage_year":1,"school_year":"2026/27","pathway_profile_id":"it.upper.liceo-scientifico","pathway_variant":"standard","curriculum_profile_ids":[]},
            {"school_stage":"upper_secondary","stage_year":4,"school_year":"2026/27","pathway_profile_id":"it.upper.tecnico-informatica-4y","pathway_variant":"quadriennale_filiera","curriculum_profile_ids":[]},
        )
        for index, context in enumerate(sample_contexts, 1):
            require_valid(context_validator, context, f"academic context fixture {index}")
        require_invalid(context_validator, {"school_stage":"middle_school","stage_year":4,"school_year":"2026/27"}, "middle-school year 4")
        require_invalid(context_validator, {"school_stage":"upper_secondary","stage_year":1,"school_year":"2026/27","pathway_profile_id":None,"pathway_variant":"standard"}, "upper-secondary null profile")
        require_invalid(context_validator, {"school_stage":"upper_secondary","stage_year":1,"school_year":"2026/27","pathway_profile_id":"it.upper.liceo-scientifico","pathway_variant":None}, "upper-secondary null variant")

        snapshot_validator = Draft202012Validator(schemas["learning-snapshot.schema.json"])
        base_subject = {"typical_year":3,"competency_states":{},"evidence_events":[],"objective_stack":None,"last_recommendation":None}
        recent = {"session_ids":[],"fingerprints":[]}
        v01 = {"version":"0.1","subjects":{"mathematics":copy.deepcopy(base_subject)},"recent_activity":recent,"preferences":{}}
        require_valid(snapshot_validator, v01, "legacy snapshot 0.1")
        bad_v01_year = copy.deepcopy(v01)
        bad_v01_year["subjects"]["mathematics"]["typical_year"] = 4
        require_invalid(snapshot_validator, bad_v01_year, "snapshot 0.1 year 4")
        bad_v01_context = copy.deepcopy(v01)
        bad_v01_context["academic_context"] = sample_contexts[1]
        require_invalid(snapshot_validator, bad_v01_context, "snapshot 0.1 with academic_context")

        v02 = copy.deepcopy(v01)
        v02["version"] = "0.2"
        v02["academic_context"] = sample_contexts[1]
        v02["subjects"]["mathematics"]["typical_year"] = 1
        require_valid(snapshot_validator, v02, "upper-secondary snapshot 0.2")
        bad_v02 = copy.deepcopy(v02)
        del bad_v02["academic_context"]
        require_invalid(snapshot_validator, bad_v02, "snapshot 0.2 without academic_context")

    if failures:
        print("Upper Secondary schema validation: FAILED")
        for failure in failures:
            print("-", failure)
        return 1

    print("Upper Secondary schema validation: OK")
    print("Schemas parsed:", len(schemas))
    print("Graph files parsed:", len(graphs))
    print("Negative schema cases: covered")
    print("Snapshot 0.1/0.2 invariants: covered")
    print("jsonschema Draft 2020-12:", "used" if Draft202012Validator is not None else "not installed; structural checks only")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
