from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods

# agents/planning_agent.py

from agents.base_agent import BaseAgent


class PlanningAgent(BaseAgent):
    name = "planner"

    def can_handle(self, task: str) -> bool:
        return "plan" in task.lower() or "planner" in task.lower()

    def handle_task(self, task: str) -> str:
        return f"🧠 PlanningAgent handled task: {task}"
