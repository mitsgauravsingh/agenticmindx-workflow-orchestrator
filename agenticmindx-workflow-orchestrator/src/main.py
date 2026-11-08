"""Run a safe, local workflow-orchestration demo."""
from orchestrator import Orchestrator, ToolRegistry


def greet(name: str) -> str:
    return f"Hello, {name}. Your local workflow is ready."


def create_summary(text: str) -> str:
    return f"Summary: {text[:120]}"


def main() -> None:
    tools = ToolRegistry()
    tools.register("greet", greet)
    tools.register("summarize", create_summary)

    workflow = [
        {"tool": "greet", "args": {"name": "AgenticMindX"}},
        {"tool": "summarize", "args": {"text": "Explore reliable, transparent, human-supervised agentic automation."}},
    ]
    result = Orchestrator(tools, max_retries=2).run("Demonstrate a safe workflow", workflow)
    print(f"Run status: {result['status']}")
    for item in result["tasks"]:
        print(f"- {item['tool']}: {item['status']} — {item.get('output', item.get('error', ''))}")


if __name__ == "__main__":
    main()
