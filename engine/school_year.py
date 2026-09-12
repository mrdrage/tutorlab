from __future__ import annotations


def start_year(value):
    text = str(value)
    if len(text) != 7 or text[4] != "/" or not text[:4].isdigit() or not text[5:].isdigit():
        raise ValueError(f"invalid school year: {value}")
    return int(text[:4])


def is_effective(document, school_year):
    current = start_year(school_year)
    start = start_year(document.get("effective_from_school_year", school_year))
    end_value = document.get("effective_to_school_year")
    end = start_year(end_value) if end_value else None
    return current >= start and (end is None or current <= end)
