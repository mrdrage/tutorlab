#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from engine.session_engine import build_session, load_policy, student_view
from engine.session_quality import validate_session
from engine.task_families import build_unique_task, supported_competencies

ACTIONS = ("recover", "consolidate", "advance", "extend", "reassess")
SUBJECTS = {
    "italian": {"prefix": "ita.", "expected": 45, "cefr": None},
    "french": {"prefix": "fr.", "expected": 46, "cefr": "A1"},
    "spanish": {"prefix": "es.", "expected": 46, "cefr": "A1"},
}
REQUIRED_NODE = {"id", "title", "strand", "typical_year", "priority", "prerequisites", "objectives", "mastery_evidence"}
REQUIRED_TASK = {"task_id", "family_id", "prompt", "response_mode", "challenge_band", "support_level", "solution", "rubric", "evidence_dimensions", "generation_parameters", "fingerprint", "competency_id"}
RESOURCE_STRANDS = {"grammar", "vocabulary", "phonology"}


def load_subject(subject: str):
    base = ROOT / "curriculum" / "middle-school" / subject
    for year in (1, 2, 3):
        data = json.loads((base / f"year-{year}.json").read_text(encoding="utf-8"))
        yield year, data


def has_cycle(nodes: list[dict]) -> bool:
    ids = {node["id"] for node in nodes}
    graph = {node["id"]: [p for p in node.get("prerequisites", []) if p in ids] for node in nodes}
    visiting = set()
    visited = set()

    def visit(node_id):
        if node_id in visiting:
            return True
        if node_id in visited:
            return False
        visiting.add(node_id)
        for prerequisite in graph.get(node_id, []):
            if visit(prerequisite):
                return True
        visiting.remove(node_id)
        visited.add(node_id)
        return False

    return any(visit(node_id) for node_id in graph if node_id not in visited)


def main() -> int:
    failures = []
    registry = supported_competencies()
    policy = load_policy()
    totals = {}
    variants = 0

    if (ROOT / ".github" / "workflows").exists():
        failures.append("GitHub workflows directory exists: validation must remain local/manual")

    for subject, config in SUBJECTS.items():
        nodes = []
        seen = set()
        for year, data in load_subject(subject):
            if data.get("subject") != subject:
                failures.append(f"{subject}/year-{year}: wrong subject metadata")
            if int(data.get("typical_year", 0)) != year:
                failures.append(f"{subject}/year-{year}: wrong typical_year")
            if config["cefr"] and data.get("target_cefr") != config["cefr"]:
                failures.append(f"{subject}/year-{year}: target_cefr must be {config['cefr']}")
            for node in data.get("nodes", []):
                nodes.append(node)
                missing = REQUIRED_NODE - set(node)
                if missing:
                    failures.append(f"{node.get('id', subject)}: missing node fields {sorted(missing)}")
                node_id = node.get("id", "")
                if not node_id.startswith(config["prefix"]):
                    failures.append(f"{node_id}: wrong id prefix")
                if node_id in seen:
                    failures.append(f"{node_id}: duplicate id")
                seen.add(node_id)
                if int(node.get("typical_year", 0)) != year:
                    failures.append(f"{node_id}: node typical_year does not match file")
                if config["cefr"] and node.get("cefr_anchor") != "A1":
                    failures.append(f"{node_id}: second-language node must be anchored to A1")
                if not node.get("objectives") or not node.get("mastery_evidence"):
                    failures.append(f"{node_id}: empty objectives/mastery evidence")

        totals[subject] = len(nodes)
        if len(nodes) != config["expected"]:
            failures.append(f"{subject}: {len(nodes)} nodes != expected {config['expected']}")

        all_ids = {node["id"] for node in nodes}
        node_index = {node["id"]: node for node in nodes}
        for node in nodes:
            for prerequisite in node.get("prerequisites", []):
                if prerequisite not in all_ids:
                    failures.append(f"{node['id']}: missing prerequisite {prerequisite}")
        if has_cycle(nodes):
            failures.append(f"{subject}: prerequisite cycle detected")

        missing_registry = sorted(all_ids - registry)
        if missing_registry:
            failures.append(f"{subject}: uncovered generation nodes: {missing_registry}")

        for index, competency_id in enumerate(sorted(all_ids), 1):
            node = node_index[competency_id]
            advance_session = None
            for offset, action in enumerate(ACTIONS, 1):
                variants += 1
                try:
                    session = build_session(
                        competency_id,
                        action,
                        seed=60_000 + index * 10 + offset,
                        challenge_band=3,
                        policy=policy,
                    )
                except Exception as exc:
                    failures.append(f"{competency_id}/{action}: build failed: {exc}")
                    continue

                if action == "advance":
                    advance_session = session

                quality_errors = validate_session(session, policy)
                if quality_errors:
                    failures.append(f"{competency_id}/{action}: quality errors: {quality_errors}")

                task_count = 0
                for phase in session.get("phases", []):
                    for item in phase.get("tasks", []):
                        task_count += 1
                        missing_task = REQUIRED_TASK - set(item)
                        if missing_task:
                            failures.append(f"{competency_id}/{action}: missing task fields {sorted(missing_task)}")
                        if not item.get("prompt") or not item.get("rubric"):
                            failures.append(f"{competency_id}/{action}: empty prompt or rubric")
                if not task_count:
                    failures.append(f"{competency_id}/{action}: no tasks generated")

                for phase in student_view(session).get("phases", []):
                    for item in phase.get("tasks", []):
                        leaked = [key for key in ("solution", "rubric", "generation_parameters", "error_signals") if key in item]
                        if leaked:
                            failures.append(f"{competency_id}/{action}: student view leaks {leaked}")

            # Semantic quality gate: a worked example must actually contain an explicit model.
            if advance_session:
                worked = [p for p in advance_session.get("phases", []) if p.get("kind") == "worked_example"]
                if not worked or not worked[0].get("tasks"):
                    failures.append(f"{competency_id}: missing worked-example task")
                else:
                    prompt = worked[0]["tasks"][0].get("prompt", "").lower()
                    if "modello" not in prompt:
                        failures.append(f"{competency_id}: worked example does not expose a model")

                if node.get("strand") == "listening":
                    tutor_tasks = [
                        item
                        for phase in advance_session.get("phases", [])
                        for item in phase.get("tasks", [])
                        if item.get("family_id", "").endswith(".listening")
                    ]
                    if not tutor_tasks or not any(item.get("solution", {}).get("tutor_script") for item in tutor_tasks):
                        failures.append(f"{competency_id}: listening task lacks tutor-only script")

            # Language resources must use concrete material, not only a generic instruction.
            if node.get("strand") in RESOURCE_STRANDS:
                item = build_unique_task(competency_id, "independent_practice", 71_001, 3, "none", "resource-check", [], 12)
                sample = item.get("generation_parameters", {}).get("sample")
                if not sample or sample not in item.get("prompt", ""):
                    failures.append(f"{competency_id}: language-resource task lacks concrete sample")

            # Anti-repeat headroom: representative seeds must not collapse to one or two fingerprints.
            fingerprints = {
                build_unique_task(competency_id, "independent_practice", 80_000 + seed, 3, "none", "diversity-check", [], 12)["fingerprint"]
                for seed in range(1, 9)
            }
            if len(fingerprints) < 3:
                failures.append(f"{competency_id}: generation diversity too low ({len(fingerprints)}/8 fingerprints)")

    if failures:
        print("Language Expansion validation: FAILED")
        for failure in failures:
            print("-", failure)
        return 1

    print("Language Expansion validation: OK")
    print(f"Italian nodes: {totals['italian']}")
    print(f"French nodes: {totals['french']}")
    print(f"Spanish nodes: {totals['spanish']}")
    print(f"Total new executable nodes: {sum(totals.values())}")
    print(f"Adaptive session variants exercised: {variants}")
    print("Semantic worked-example checks: OK")
    print("Concrete language-resource checks: OK")
    print("Generation diversity checks: OK")
    print("Listening tutor-script isolation: OK")
    print("GitHub Actions/workflows: absent")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
