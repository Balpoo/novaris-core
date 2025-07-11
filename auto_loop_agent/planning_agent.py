from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods

# agents/planning_agent.py


class PlanningAgent:
    def __init__(self):
        self.name = "PlanningAgent"

    def run(self, task: str):
        return f"🗓️ [PlanningAgent] Created strategic plan for: '{task}'"
