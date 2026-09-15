#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from typing import Any

from engine.tutor_service import hub_plan, hub_transition


def _read_request() -> dict[str, Any]:
    raw = sys.stdin.read()
    if not raw.strip():
        raise ValueError("empty bridge request")
    value = json.loads(raw)
    if not isinstance(value, dict):
        raise ValueError("bridge request must be an object")
    return value


def _dispatch(request: dict[str, Any]) -> dict[str, Any]:
    operation = request.get("operation")
    payload = request.get("payload")
    if not isinstance(payload, dict):
        raise ValueError("payload must be an object")

    if operation == "plan":
        seed = request.get("seed", 1)
        if isinstance(seed, bool) or not isinstance(seed, int):
            raise ValueError("seed must be an integer")
        return hub_plan(payload, seed=seed)
    if operation == "transition":
        return hub_transition(payload)
    raise ValueError("unsupported bridge operation")


def main() -> int:
    try:
        result = _dispatch(_read_request())
        sys.stdout.write(json.dumps({"ok": True, "result": result}, ensure_ascii=False))
        sys.stdout.write("\n")
        return 0
    except Exception as exc:  # boundary CLI: serialize errors, never a traceback as protocol
        sys.stdout.write(
            json.dumps(
                {
                    "ok": False,
                    "error": {
                        "type": type(exc).__name__,
                        "message": str(exc),
                    },
                },
                ensure_ascii=False,
            )
        )
        sys.stdout.write("\n")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
