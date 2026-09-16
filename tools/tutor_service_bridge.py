#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from engine.tutor_service import hub_plan, hub_transition

BRIDGE_VERSION = "1.0"


class BridgeProtocolError(ValueError):
    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code


def _read_request() -> dict[str, Any]:
    raw = sys.stdin.read()
    if not raw.strip():
        raise BridgeProtocolError("EMPTY_REQUEST", "empty bridge request")
    try:
        value = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise BridgeProtocolError("INVALID_JSON", "bridge request is not valid JSON") from exc
    if not isinstance(value, dict):
        raise BridgeProtocolError("INVALID_ENVELOPE", "bridge request must be an object")
    return value


def _dispatch(request: dict[str, Any]) -> dict[str, Any]:
    if request.get("bridge_version") != BRIDGE_VERSION:
        raise BridgeProtocolError("UNSUPPORTED_BRIDGE_VERSION", "unsupported bridge version")

    operation = request.get("operation")
    if operation not in {"plan", "transition"}:
        raise BridgeProtocolError("UNSUPPORTED_OPERATION", "unsupported bridge operation")

    allowed_fields = {"bridge_version", "operation", "payload"}
    if operation == "plan":
        allowed_fields.add("seed")
    unknown_fields = set(request) - allowed_fields
    if unknown_fields:
        raise BridgeProtocolError(
            "INVALID_ENVELOPE",
            f"unsupported bridge fields: {sorted(unknown_fields)}",
        )

    payload = request.get("payload")
    if not isinstance(payload, dict):
        raise BridgeProtocolError("INVALID_PAYLOAD", "payload must be an object")

    if operation == "plan":
        seed = request.get("seed", 1)
        if isinstance(seed, bool) or not isinstance(seed, int):
            raise BridgeProtocolError("INVALID_SEED", "seed must be an integer")
        return hub_plan(payload, seed=seed)

    return hub_transition(payload)


def _write_success(result: dict[str, Any]) -> None:
    sys.stdout.write(
        json.dumps(
            {
                "bridge_version": BRIDGE_VERSION,
                "ok": True,
                "result": result,
            },
            ensure_ascii=False,
        )
    )
    sys.stdout.write("\n")


def _write_error(code: str, exc: Exception, *, public_message: str | None = None) -> None:
    sys.stdout.write(
        json.dumps(
            {
                "bridge_version": BRIDGE_VERSION,
                "ok": False,
                "error": {
                    "code": code,
                    "type": type(exc).__name__,
                    "message": public_message if public_message is not None else str(exc),
                },
            },
            ensure_ascii=False,
        )
    )
    sys.stdout.write("\n")


def main() -> int:
    try:
        result = _dispatch(_read_request())
        _write_success(result)
        return 0
    except BridgeProtocolError as exc:
        _write_error(exc.code, exc)
        return 1
    except (ValueError, KeyError, TypeError) as exc:
        _write_error("TUTORLAB_VALIDATION_ERROR", exc)
        return 1
    except Exception as exc:  # boundary CLI: never serialize an internal traceback as protocol
        _write_error("INTERNAL_ERROR", exc, public_message="unexpected bridge error")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
