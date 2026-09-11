import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_competency(competency_id):
    if competency_id.startswith("math."):
        folder = "mathematics"
    elif competency_id.startswith("eng."):
        folder = "english"
    else:
        raise ValueError("unsupported competency")
    base = ROOT / "curriculum" / "middle-school" / folder
    for year in (1, 2, 3):
        data = json.loads((base / f"year-{year}.json").read_text(encoding="utf-8"))
        for node in data.get("nodes", []):
            if node.get("id") == competency_id:
                return node
    raise ValueError("competency not found")


def subject_for_competency(competency_id):
    return "mathematics" if competency_id.startswith("math.") else "english"
