import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

PREFIX_TO_SUBJECT = {
    "math.": "mathematics",
    "eng.": "english",
    "ita.": "italian",
    "fr.": "french",
    "es.": "spanish",
}


def subject_for_competency(competency_id):
    for prefix, subject in PREFIX_TO_SUBJECT.items():
        if competency_id.startswith(prefix):
            return subject
    raise ValueError("unsupported competency")


def load_competency(competency_id):
    folder = subject_for_competency(competency_id)
    base = ROOT / "curriculum" / "middle-school" / folder
    for year in (1, 2, 3):
        data = json.loads((base / f"year-{year}.json").read_text(encoding="utf-8"))
        for node in data.get("nodes", []):
            if node.get("id") == competency_id:
                return node
    raise ValueError("competency not found")
