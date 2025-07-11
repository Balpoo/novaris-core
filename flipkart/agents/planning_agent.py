from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods


class PlanningAgent:
    def can_handle(self, task: str) -> bool:
        return (
            "plan" in task.lower()
            or "create" in task.lower()
            or "design" in task.lower()
        )

    def handle(self, task: str):
        result = f"Planned step-by-step execution for: {task}"
        confidence = 0.92
        return result, confidence, "PlanningAgent"
