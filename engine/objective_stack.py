from __future__ import annotations

from copy import deepcopy
from typing import Any


def start_objective(target_competency_id: str) -> dict[str, Any]:
    return {
        "root_target_id": target_competency_id,
        "frames": [
            {
                "competency_id": target_competency_id,
                "kind": "target",
                "reason": "requested_or_selected_target",
            }
        ],
    }


def current_objective(stack: dict[str, Any]) -> str:
    frames = stack.get("frames", [])
    if not frames:
        raise ValueError("Objective stack vuoto")
    return str(frames[-1]["competency_id"])


def recovery_depth(stack: dict[str, Any]) -> int:
    return sum(1 for frame in stack.get("frames", []) if frame.get("kind") == "recovery")


def push_recovery(
    stack: dict[str, Any],
    recovery_competency_id: str,
    *,
    reason: str,
    max_depth: int,
) -> dict[str, Any]:
    if recovery_depth(stack) >= max_depth:
        raise ValueError("Profondità massima di recupero raggiunta")

    updated = deepcopy(stack)
    updated["frames"].append(
        {
            "competency_id": recovery_competency_id,
            "kind": "recovery",
            "reason": reason,
            "return_to": current_objective(stack),
        }
    )
    return updated


def complete_current(stack: dict[str, Any]) -> dict[str, Any]:
    """Complete the current frame and return to the suspended objective.

    The root target cannot be popped by this function. Completing it is a session-level
    outcome handled by the future session engine.
    """
    updated = deepcopy(stack)
    frames = updated.get("frames", [])
    if len(frames) <= 1:
        raise ValueError("Il target radice non può essere rimosso dallo stack")
    frames.pop()
    return updated
