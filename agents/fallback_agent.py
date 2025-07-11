# agents/fallback_agent.py

from core.gpt_fallback import call_gpt


class GPTFallbackAgent:
    def __init__(self, name="GPTFallback", role="Assistant"):
        self.name = name
        self.role = role

    def run(self, user_input: str, context: str = "") -> str:
        prompt = f"{context}\n\nUser Query: {user_input}"
        return call_gpt(prompt)
