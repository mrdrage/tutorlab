#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from engine.objective_stack import start_objective
from engine.result_transition import transition
from engine.session_engine import build_session, load_policy, student_view
from engine.session_quality import validate_session
from engine.task_families import build_unique_task, supported_competencies

ACTIONS = ("recover", "consolidate", "advance", "extend", "reassess")
SUBJECTS = {
    "italian": {"prefix": "ita.", "expected": 45, "cefr": None},
    "french": {"prefix": "fr.", "expected": 46, "cefr": "A1"},
    "spanish": {"prefix": "es.", "expected": 46, "cefr": "A1"},
}
PIPELINE_TARGETS = {
    "italian": "ita.grammar.orthography-punctuation",
    "french": "fr.grammar.identity-possession",
    "spanish": "es.grammar.identity-possession",
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


def _synthetic_snapshot(subject: str, target: str) -> dict:
    return {
        "version": "0.1",
        "subjects": {
            subject: {
                "typical_year": 1,
                "competency_states": {},
                "evidence_events": [],
                "objective_stack": start_objective(target),
                "last_recommendation": None,
            }
        },
        "recent_activity": {"session_ids": [], "fingerprints": []},
        "preferences": {},
    }


def _scored_result(session: dict) -> dict:
    responses = []
    for phase in session.get("phases", []):
        for item in phase.get("tasks", []):
            row = {
                "task_id": item["task_id"],
                "response": "synthetic scored response",
                "status": "correct",
                "score": 1.0,
                "support_used": item.get("support_level", "none"),
                "explanation_quality": 0.85,
            }
            if phase.get("kind") in {"transfer", "transfer_probe", "challenge"}:
                row["transfer_success"] = 0.9
            responses.append(row)
    return {
        "version": "0.1",
        "session_id": session["session_id"],
        "completed_at": "2026-09-11T22:30:00+02:00",
        "completion_status": "completed",
        "responses": responses,
    }


def _check_pipeline(subject: str, target: str, adaptive_policy: dict, session_policy: dict) -> list[str]:
    failures = []
    snapshot = _synthetic_snapshot(subject, target)
    session = build_session(target, "consolidate", original_target_id=target, seed=91_000, challenge_band=2, policy=session_policy)
    moved = transition(snapshot, subject, session, _scored_result(session), adaptive_policy)
    updated = moved.get("snapshot_update", {})
    subject_state = updated.get("subjects", {}).get(subject, {})
    events = moved.get("evidence_events", [])

    if not events:
        failures.append(f"{subject}: session results did not become evidence events")
    if moved.get("pending_task_ids"):
        failures.append(f"{subject}: explicitly scored synthetic responses unexpectedly remained pending")
    if target not in subject_state.get("competency_states", {}):
        failures.append(f"{subject}: competency state not updated after evidence")
    if session["session_id"] not in updated.get("recent_activity", {}).get("session_ids", []):
        failures.append(f"{subject}: session history not updated")
    if not updated.get("recent_activity", {}).get("fingerprints", []):
        failures.append(f"{subject}: fingerprint history not updated")
    next_step = moved.get("next_step", {})
    if next_step.get("action") not in {"recover", "consolidate", "advance", "extend", "reassess", "return_to"}:
        failures.append(f"{subject}: invalid next-step action after transition: {next_step}")
    return failures


def main() -> int:
    failures = []
    registry = supported_competencies()
    session_policy = load_policy()
    adaptive_policy = json.loads((ROOT / "config" / "adaptive-policy.json").read_text(encoding="utf-8"))
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
                        policy=session_policy,
                    )
                except Exception as exc:
                    failures.append(f"{competency_id}/{action}: build failed: {exc}")
                    continue

                if action == "advance":
                    advance_session = session

                quality_errors = validate_session(session, session_policy)
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

            if node.get("strand") in RESOURCE_STRANDS:
                item = build_unique_task(competency_id, "independent_practice", 71_001, 3, "none", "resource-check", [], 12)
                sample = item.get("generation_parameters", {}).get("sample")
                if not sample or sample not in item.get("prompt", ""):
                    failures.append(f"{competency_id}: language-resource task lacks concrete sample")

            fingerprints = {
                build_unique_task(competency_id, "independent_practice", 80_000 + seed, 3, "none", "diversity-check", [], 12)["fingerprint"]
                for seed in range(1, 9)
            }
            if len(fingerprints) < 3:
                failures.append(f"{competency_id}: generation diversity too low ({len(fingerprints)}/8 fingerprints)")

    for subject, target in PIPELINE_TARGETS.items():
        failures.extend(_check_pipeline(subject, target, adaptive_policy, session_policy))

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
    print("Language end-to-end transitions: OK")
    print("GitHub Actions/workflows: absent")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
