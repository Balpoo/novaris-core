from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods


class MemoryAgent:
    def can_handle(self, task: str) -> bool:
        return "remember" in task.lower() or "log" in task.lower()

    def handle(self, task: str):
        result = f"Memory log created for task: {task}"
        confidence = 0.95
        return result, confidence, "MemoryAgent"
