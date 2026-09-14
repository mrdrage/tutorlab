import json
from functools import lru_cache
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


def _middle_competencies(subject):
    base = ROOT / "curriculum" / "middle-school" / subject
    if not base.exists():
        return
    for year in (1, 2, 3):
        path = base / f"year-{year}.json"
        if not path.exists():
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        for node in data.get("nodes", []):
            yield node


def _upper_competencies(subject):
    base = ROOT / "curriculum" / "upper-secondary" / subject
    if not base.exists():
        return
    seen = set()
    for path in sorted(base.rglob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        for node in data.get("nodes", []):
            cid = node.get("id")
            if cid in seen:
                raise ValueError(f"duplicate upper-secondary competency id: {cid}")
            seen.add(cid)
            yield node


@lru_cache(maxsize=None)
def _index(subject):
    result = {}
    for node in _middle_competencies(subject) or ():
        result[node["id"]] = node
    for node in _upper_competencies(subject) or ():
        if node["id"] in result:
            raise ValueError(f"duplicate competency id across stages: {node['id']}")
        result[node["id"]] = node
    return result


def load_competency(competency_id):
    subject = subject_for_competency(competency_id)
    node = _index(subject).get(competency_id)
    if node is None:
        raise ValueError("competency not found")
    return node
