from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods

# agents/content_agent.py


class ContentAgent:
    def __init__(self):
        self.name = "ContentAgent"

    def run(self, task: str):
        return f"📝 [ContentAgent] Created high-quality text for: '{task}'"
