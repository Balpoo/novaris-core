from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods

# agents/memory_agent.py

from agents.agent_base import Agent


class MemoryAgent(Agent):
    def __init__(self):
        super().__init__(
            name="MemoryAgent", role="Recall Specialist", tone="reflective"
        )

    def can_handle(self, task: str) -> bool:
        return "recall" in task.lower() or "what do you remember" in task.lower()

    def execute(self, task: str) -> str:
        if self.memory.entries:
            result = "\n".join(f"🧠 {item}" for item in self.memory.entries[-5:])
        else:
            result = "I don't remember anything yet."
        self.memory.remember(task, result)
        self.persona.adjust_emotion("success" if self.memory.entries else "neutral")
        return self._styled_response(result)
