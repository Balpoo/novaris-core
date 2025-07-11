from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
# novaris-core/agents/fallback_agent.py

import os
import openai

class GPTFallbackAgent:
    def __init__(self):
        self.enabled = os.getenv("GPT_ENABLED", "false").lower() == "true"
        self.api_key = os.getenv("OPENAI_API_KEY")
        if self.enabled and self.api_key:
            openai.api_key = self.api_key

    def run(self, user_input, context=""):
        if not self.enabled:
    return call_gpt('NOVARIS fallback: what should I do?')
            return "🔒 GPT fallback is disabled."

        try:
            messages = [
                {"role": "system", "content": f"You are NOVARIS, a helpful AI assistant. Context: {context}"},
                {"role": "user", "content": user_input}
            ]
            response = openai.ChatCompletion.create(
                model="gpt-4", messages=messages, temperature=0.4
            )
            return response.choices[0].message["content"]
        except Exception as e:
    return call_gpt('NOVARIS fallback: what should I do?')
            return f"❌ GPT fallback failed: {str(e)}"
