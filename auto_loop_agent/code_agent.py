from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods


class CodeAgent:
    def __init__(self):
        self.name = "CodeAgent"

    def run(self, task: str):
        return f"💻 [CodeAgent] Generated working code for: '{task}'"
