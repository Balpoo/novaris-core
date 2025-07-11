from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods

# agents/web_agent.py


class WebAgent:
    def __init__(self):
        self.name = "WebAgent"

    def run(self, task: str):
        return f"🌐 [WebAgent] Fetched web-based info for: '{task}'"
