# AgenticMindX Workflow Orchestrator

A small, dependency-free Python project demonstrating a practical foundation for agentic workflows: accept a goal, create a task plan, execute registered tools, retry failures, and write an auditable run log.

## What it demonstrates
- A simple planner that turns a goal into ordered tasks.
- A tool registry with explicit, allow-listed actions.
- Retry handling and clear task status reporting.
- JSON run logs for traceability.

## Quick start
Requires Python 3.10 or newer.

```bash
python src/main.py
```

The demo runs a harmless local workflow and writes `run_log.json`.

## Project status
Starter prototype. The planner is intentionally deterministic; it does not call an external AI model or perform actions outside this repository.

## Next steps
1. Add an LLM-backed planner behind the existing planner interface.
2. Add human approval before sensitive tools run.
3. Add unit tests and persistent run storage.
4. Add integrations only with explicit credentials and permissions.

## Safety
Tools are allow-listed. Do not add destructive or external actions without authentication, authorization, input validation, and human review.
