from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods

# utils/task_router.py - Placeholder implementation


# Utility to route tasks (for future dynamic logic)
def route_task(task: str) -> str:
    if "plan" in task:
        return "PlanningAgent"
    elif "file" in task:
        return "FilingAgent"
    return "MemoryAgent"
