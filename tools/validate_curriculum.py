#!/usr/bin/env python3
"""Validazione strutturale dei curriculum TutorLab.

Usa solo la standard library. Esecuzione dalla root del repository:

    python3 tools/validate_curriculum.py
"""

from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MATH_DIR = ROOT / "curriculum" / "middle-school" / "mathematics"
YEAR_FILES = [MATH_DIR / f"year-{year}.json" for year in (1, 2, 3)]
LINKS_FILE = MATH_DIR / "cross-year-links.json"
ALLOWED_STRANDS = {
    "numbers",
    "geometry",
    "relations_functions",
    "data_probability",
    "mathematical_practices",
}
ALLOWED_PRIORITIES = {"gateway", "core", "supporting", "extension"}


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def load_json(path: Path, errors: list[str]) -> dict:
    try:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except FileNotFoundError:
        fail(errors, f"File mancante: {path.relative_to(ROOT)}")
    except json.JSONDecodeError as exc:
        fail(
            errors,
            f"JSON non valido in {path.relative_to(ROOT)}: "
            f"riga {exc.lineno}, colonna {exc.colno}: {exc.msg}",
        )
    return {}


def detect_cycles(nodes: dict[str, dict]) -> list[list[str]]:
    graph: dict[str, list[str]] = defaultdict(list)
    for node_id, node in nodes.items():
        for prerequisite in node.get("prerequisites", []):
            if prerequisite in nodes:
                graph[prerequisite].append(node_id)

    state: dict[str, int] = {}
    stack: list[str] = []
    cycles: list[list[str]] = []

    def visit(node_id: str) -> None:
        state[node_id] = 1
        stack.append(node_id)
        for child in graph[node_id]:
            child_state = state.get(child, 0)
            if child_state == 0:
                visit(child)
            elif child_state == 1:
                start = stack.index(child)
                cycles.append(stack[start:] + [child])
        stack.pop()
        state[node_id] = 2

    for node_id in nodes:
        if state.get(node_id, 0) == 0:
            visit(node_id)

    return cycles


def main() -> int:
    errors: list[str] = []
    nodes: dict[str, dict] = {}
    node_sources: dict[str, str] = {}
    year_counts: Counter[int] = Counter()
    strand_counts: Counter[str] = Counter()

    for expected_year, path in enumerate(YEAR_FILES, start=1):
        data = load_json(path, errors)
        if not data:
            continue

        if data.get("subject") != "mathematics":
            fail(errors, f"{path.name}: subject deve essere mathematics")
        if data.get("school_stage") != "middle_school":
            fail(errors, f"{path.name}: school_stage deve essere middle_school")
        if data.get("typical_year") != expected_year:
            fail(
                errors,
                f"{path.name}: typical_year={data.get('typical_year')} ma atteso {expected_year}",
            )

        file_nodes = data.get("nodes")
        if not isinstance(file_nodes, list) or not file_nodes:
            fail(errors, f"{path.name}: nodes deve essere una lista non vuota")
            continue

        for index, node in enumerate(file_nodes):
            context = f"{path.name} nodo #{index + 1}"
            node_id = node.get("id")
            if not isinstance(node_id, str) or not node_id.startswith("math."):
                fail(errors, f"{context}: id non valido: {node_id!r}")
                continue
            if node_id in nodes:
                fail(
                    errors,
                    f"ID duplicato {node_id}: {node_sources[node_id]} e {path.name}",
                )
                continue

            nodes[node_id] = node
            node_sources[node_id] = path.name
            year_counts[node.get("typical_year")] += 1
            strand_counts[node.get("strand")] += 1

            if node.get("typical_year") != expected_year:
                fail(
                    errors,
                    f"{node_id}: typical_year={node.get('typical_year')} ma si trova in {path.name}",
                )
            if node.get("strand") not in ALLOWED_STRANDS:
                fail(errors, f"{node_id}: strand non riconosciuto: {node.get('strand')}")
            if node.get("priority") not in ALLOWED_PRIORITIES:
                fail(errors, f"{node_id}: priority non riconosciuta: {node.get('priority')}")
            if not node.get("objectives"):
                fail(errors, f"{node_id}: manca objectives")
            if not node.get("mastery_evidence"):
                fail(errors, f"{node_id}: manca mastery_evidence")
            if not isinstance(node.get("prerequisites"), list):
                fail(errors, f"{node_id}: prerequisites deve essere una lista")

    for node_id, node in nodes.items():
        for prerequisite in node.get("prerequisites", []):
            if prerequisite not in nodes:
                fail(errors, f"{node_id}: prerequisito inesistente {prerequisite}")
            elif prerequisite == node_id:
                fail(errors, f"{node_id}: auto-prerequisito non consentito")

    for cycle in detect_cycles(nodes):
        fail(errors, "Ciclo nei prerequisiti: " + " -> ".join(cycle))

    links_data = load_json(LINKS_FILE, errors)
    if links_data:
        for index, link in enumerate(links_data.get("gateway_links", []), start=1):
            source = link.get("from")
            if source not in nodes:
                fail(errors, f"gateway link #{index}: sorgente inesistente {source}")
            for target in link.get("to", []):
                if target not in nodes:
                    fail(errors, f"gateway link #{index}: destinazione inesistente {target}")
            if not link.get("recovery_rule"):
                fail(errors, f"gateway link #{index}: manca recovery_rule")

    required_strands = ALLOWED_STRANDS
    missing_strands = required_strands - set(strand_counts)
    if missing_strands:
        fail(errors, f"Nuclei senza nodi: {sorted(missing_strands)}")

    for year in (1, 2, 3):
        if year_counts[year] == 0:
            fail(errors, f"Nessun nodo per l'anno {year}")

    if errors:
        print("Curriculum validation: FAILED")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Curriculum validation: OK")
    print(f"Nodes: {len(nodes)}")
    print("By year:", dict(sorted(year_counts.items())))
    print("By strand:", dict(sorted(strand_counts.items())))
    print(f"Gateway links: {len(links_data.get('gateway_links', []))}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
