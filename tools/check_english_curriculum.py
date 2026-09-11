#!/usr/bin/env python3
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
base = root / "curriculum" / "middle-school" / "english"
files = [base / f"year-{n}.json" for n in (1, 2, 3)]
errors = []
nodes = {}

for year, path in enumerate(files, 1):
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"{path.name}: {exc}")
        continue
    if data.get("subject") != "english" or data.get("typical_year") != year:
        errors.append(f"{path.name}: metadata incoerenti")
    for node in data.get("nodes", []):
        node_id = node.get("id")
        if not isinstance(node_id, str) or not node_id.startswith("eng."):
            errors.append(f"{path.name}: id non valido {node_id!r}")
            continue
        if node_id in nodes:
            errors.append(f"ID duplicato: {node_id}")
        nodes[node_id] = node
        if node.get("typical_year") != year:
            errors.append(f"{node_id}: anno incoerente")
        if node.get("cefr_anchor") not in {"A1", "A2"}:
            errors.append(f"{node_id}: cefr_anchor non valido")
        if not node.get("objectives") or not node.get("mastery_evidence"):
            errors.append(f"{node_id}: obiettivi/evidenze mancanti")

for node_id, node in nodes.items():
    for pre in node.get("prerequisites", []):
        if pre not in nodes:
            errors.append(f"{node_id}: prerequisito inesistente {pre}")
        if pre == node_id:
            errors.append(f"{node_id}: auto-prerequisito")

links = json.loads((base / "cross-year-links.json").read_text(encoding="utf-8"))
for link in links.get("gateway_links", []):
    if link.get("from") not in nodes:
        errors.append(f"gateway sorgente inesistente: {link.get('from')}")
    for target in link.get("to", []):
        if target not in nodes:
            errors.append(f"gateway target inesistente: {target}")

if errors:
    print("English curriculum check: FAILED")
    for error in errors:
        print("-", error)
    raise SystemExit(1)

print(f"English curriculum check: OK ({len(nodes)} nodes)")
