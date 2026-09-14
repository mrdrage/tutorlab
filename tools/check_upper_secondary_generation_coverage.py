#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from engine.curriculum_access import load_competency
from engine.mastery_rubrics import rubric_for
from engine.session_engine import build_session, load_policy
from engine.session_quality import validate_session
from engine.task_families import supported_competencies
from engine.upper_secondary_resolver import curriculum_nodes, load_catalog

ACTIONS = ("recover", "consolidate", "advance", "extend", "reassess")
SUBJECTS = ("mathematics", "english")


def graph_ids(subject: str):
    base = ROOT / "curriculum" / "upper-secondary" / subject
    result = set()
    duplicates = []
    for path in sorted(base.rglob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        for node in data.get("nodes", []):
            cid = node["id"]
            if cid in result:
                duplicates.append(cid)
            result.add(cid)
    return result, duplicates


def main():
    policy = load_policy()
    registry = supported_competencies()
    catalog = load_catalog()
    failures = []
    exercised = {subject: set() for subject in SUBJECTS}
    variants = 0
    profile_counts = {}

    if (ROOT / ".github" / "workflows").exists():
        failures.append("GitHub workflows directory must remain absent")

    expected = {}
    for subject in SUBJECTS:
        ids, duplicates = graph_ids(subject)
        expected[subject] = ids
        if duplicates:
            failures.append(f"{subject}: duplicate graph ids {sorted(set(duplicates))}")

    for p_index, profile in enumerate(catalog.get("profiles", []), 1):
        context = {
            "school_stage": "upper_secondary",
            "stage_year": int(profile["duration_years"]),
            "school_year": "2026/27",
            "pathway_profile_id": profile["id"],
            "pathway_variant": profile["pathway_variant"],
            "curriculum_profile_ids": [],
        }
        counts = {}
        for subject in SUBJECTS:
            try:
                nodes = curriculum_nodes(subject, context)
            except Exception as exc:
                failures.append(f"{profile['id']}/{subject}: resolver failed: {exc}")
                continue
            counts[subject] = len(nodes)
            for n_index, node in enumerate(nodes, 1):
                cid = node["id"]
                exercised[subject].add(cid)
                if cid not in registry:
                    failures.append(f"{profile['id']}/{cid}: missing task family")
                    continue
                try:
                    loaded = load_competency(cid)
                except Exception as exc:
                    failures.append(f"{cid}: curriculum_access failed: {exc}")
                    continue
                if loaded.get("id") != cid:
                    failures.append(f"{cid}: loader returned wrong competency")
                family, _ = rubric_for(cid)
                if family == "generic":
                    failures.append(f"{cid}: generic mastery rubric used")
                for a_index, action in enumerate(ACTIONS, 1):
                    variants += 1
                    seed = 800000 + p_index * 10000 + n_index * 10 + a_index
                    try:
                        session = build_session(
                            cid,
                            action,
                            original_target_id=cid,
                            seed=seed,
                            challenge_band=min(5, max(2, int(node.get("stage_year", 1)) + 1)),
                            policy=policy,
                        )
                    except Exception as exc:
                        failures.append(f"{profile['id']}/{cid}/{action}: build failed: {exc}")
                        continue
                    quality = validate_session(session, policy)
                    if quality:
                        failures.append(f"{profile['id']}/{cid}/{action}: quality {quality}")
                    tasks = [task for phase in session.get("phases", []) for task in phase.get("tasks", [])]
                    if not tasks:
                        failures.append(f"{profile['id']}/{cid}/{action}: no tasks generated")
        profile_counts[profile["id"]] = counts

    for subject in SUBJECTS:
        missing = expected[subject] - exercised[subject]
        extra = exercised[subject] - expected[subject]
        if missing:
            failures.append(f"{subject}: graph nodes unreachable from every seed profile: {sorted(missing)}")
        if extra:
            failures.append(f"{subject}: resolver produced unknown nodes: {sorted(extra)}")
        uncovered = expected[subject] - registry
        if uncovered:
            failures.append(f"{subject}: registry does not cover {sorted(uncovered)}")

    if failures:
        print("Upper Secondary generation coverage: FAILED")
        for failure in failures:
            print("-", failure)
        return 1

    total = sum(len(expected[s]) for s in SUBJECTS)
    print("Upper Secondary generation coverage: OK")
    print("Unique executable upper-secondary nodes:", total)
    print("Mathematics nodes:", len(expected["mathematics"]))
    print("English nodes:", len(expected["english"]))
    print("Adaptive session variants exercised:", variants)
    print("Seed pathway profiles exercised:", len(profile_counts))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
