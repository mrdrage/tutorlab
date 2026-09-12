#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
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

        if catalog is not None:
            validator = Draft202012Validator(schemas["education-pathway.schema.json"])
            for error in validator.iter_errors(catalog):
                failures.append(f"catalog.seed.json: {error.message}")

        graph_validator = Draft202012Validator(schemas["upper-secondary-curriculum-graph.schema.json"])
        for path, graph in graphs:
            for error in graph_validator.iter_errors(graph):
                failures.append(f"{path.relative_to(ROOT)}: {error.message}")

        context_validator = Draft202012Validator(schemas["academic-context.schema.json"])
        sample_contexts = (
            {"school_stage":"middle_school","stage_year":2,"school_year":"2026/27","pathway_profile_id":None,"pathway_variant":None,"curriculum_profile_ids":[]},
            {"school_stage":"upper_secondary","stage_year":1,"school_year":"2026/27","pathway_profile_id":"it.upper.liceo-scientifico","pathway_variant":"standard","curriculum_profile_ids":[]},
            {"school_stage":"upper_secondary","stage_year":4,"school_year":"2026/27","pathway_profile_id":"it.upper.tecnico-informatica-4y","pathway_variant":"quadriennale_filiera","curriculum_profile_ids":[]},
        )
        for index, context in enumerate(sample_contexts, 1):
            for error in context_validator.iter_errors(context):
                failures.append(f"academic context fixture {index}: {error.message}")

    if failures:
        print("Upper Secondary schema validation: FAILED")
        for failure in failures:
            print("-", failure)
        return 1

    print("Upper Secondary schema validation: OK")
    print("Schemas parsed:", len(schemas))
    print("Graph files parsed:", len(graphs))
    print("jsonschema Draft 2020-12:", "used" if Draft202012Validator is not None else "not installed; structural checks only")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
