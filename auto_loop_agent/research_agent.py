from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods

# agents/research_agent.py


class ResearchAgent:
    def __init__(self):
        self.name = "ResearchAgent"

    def run(self, task: str):
        return f"🔍 [ResearchAgent] Found insights for: '{task}'"
