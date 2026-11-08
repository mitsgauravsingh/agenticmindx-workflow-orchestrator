import unittest
from src.orchestrator import Orchestrator, ToolRegistry


class OrchestratorTests(unittest.TestCase):
    def test_registered_tool_runs(self):
        registry = ToolRegistry()
        registry.register("double", lambda value: value * 2)
        result = Orchestrator(registry).run("test", [{"tool": "double", "args": {"value": 4}}])
        self.assertEqual(result["status"], "completed")
        self.assertEqual(result["tasks"][0]["output"], "8")

    def test_unknown_tool_fails_safely(self):
        result = Orchestrator(ToolRegistry()).run("test", [{"tool": "not_allowed"}])
        self.assertEqual(result["status"], "failed")


if __name__ == "__main__":
    unittest.main()
