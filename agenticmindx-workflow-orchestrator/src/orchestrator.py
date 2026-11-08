"""Minimal orchestration primitives with allow-listed tools and audit logging."""
from __future__ import annotations
import json
import time
from pathlib import Path
from typing import Any, Callable


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, Callable[..., Any]] = {}

    def register(self, name: str, function: Callable[..., Any]) -> None:
        if not name or name in self._tools:
            raise ValueError(f"Invalid or duplicate tool name: {name!r}")
        self._tools[name] = function

    def execute(self, name: str, args: dict[str, Any]) -> Any:
        if name not in self._tools:
            raise KeyError(f"Tool is not allow-listed: {name}")
        return self._tools[name](**args)


class Orchestrator:
    def __init__(self, tools: ToolRegistry, max_retries: int = 1) -> None:
        if max_retries < 0:
            raise ValueError("max_retries cannot be negative")
        self.tools = tools
        self.max_retries = max_retries

    def run(self, goal: str, plan: list[dict[str, Any]]) -> dict[str, Any]:
        tasks = []
        for index, task in enumerate(plan, start=1):
            record = {"step": index, "tool": task["tool"], "status": "failed"}
            for attempt in range(1, self.max_retries + 2):
                try:
                    output = self.tools.execute(task["tool"], task.get("args", {}))
                    record.update(status="completed", attempt=attempt, output=str(output))
                    break
                except Exception as exc:  # captured for the audit record
                    record.update(attempt=attempt, error=f"{type(exc).__name__}: {exc}")
                    if attempt > self.max_retries:
                        break
                    time.sleep(0.1)
            tasks.append(record)
            if record["status"] != "completed":
                break

        result = {
            "goal": goal,
            "status": "completed" if tasks and all(t["status"] == "completed" for t in tasks) else "failed",
            "tasks": tasks,
        }
        Path("run_log.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
        return result
