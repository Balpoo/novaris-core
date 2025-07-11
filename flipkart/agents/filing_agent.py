from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods


class FilingAgent:
    def can_handle(self, task: str) -> bool:
        return "file" in task.lower() or "submit" in task.lower()

    def handle(self, task: str):
        result = f"Filed required documents for: {task}"
        confidence = 0.87
        return result, confidence, "FilingAgent"
