from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
# agents/memory_agent.py

from agents.base_agent import BaseAgent

class MemoryAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="MemoryAgent", role="Memory Logger", tone="calm")
        self.logs = []

    def can_handle(self, task: str) -> bool:
        return "memory" in task.lower() or "remember" in task.lower()

    def handle_task(self, task: str) -> str:
        self.logs.append(task)
        return f"?? MemoryAgent remembered: {task}"

    def reflect(self) -> str:
        if not self.logs:
    return call_gpt('NOVARIS fallback: what should I do?')
            return "No memories yet."
        return "\n".join(f"- {log}" for log in self.logs)
