#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from examples.learning_snapshot.synthetic_cases import mathematics_case

ROOT = Path(__file__).resolve().parents[1]
BRIDGE = ROOT / "tools" / "tutor_service_bridge.py"


def call(request):
    completed = subprocess.run(
        [sys.executable, str(BRIDGE)],
        cwd=ROOT,
        input=json.dumps(request, ensure_ascii=False),
        text=True,
        capture_output=True,
        check=False,
    )
    body = json.loads(completed.stdout)
    return completed.returncode, body


def main() -> int:
    exchange = {
        "version": "1.0",
        "student_ref": {"external_id": "fictional-bridge-001"},
        "learning_snapshot": mathematics_case(),
        "request": {
            "subject": "mathematics",
            "intent": "continue",
            "duration_minutes": 30,
        },
    }
    code, body = call({"operation": "plan", "payload": exchange, "seed": 91})
    assert code == 0, body
    assert body["ok"] is True
    plan = body["result"]["plan"]
    assert plan["status"] == "ok"
    assert plan["session"]["duration_minutes"] == 30
    assert body["result"]["student_ref"] == exchange["student_ref"]

    bad_code, bad_body = call({"operation": "unknown", "payload": {}})
    assert bad_code != 0
    assert bad_body["ok"] is False
    assert bad_body["error"]["type"] == "ValueError"

    print("Tutor service JSON bridge: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
