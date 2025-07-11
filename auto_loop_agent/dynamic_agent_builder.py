from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
# agents/dynamic_agent_builder.py

import os
import openai
from agents.agent_base import Agent

class DynamicAgentBuilder:
    def __init__(self):
        self.enabled = os.getenv("GPT_ENABLED", "false").lower() == "true"
        self.api_key = os.getenv("OPENAI_API_KEY")
        if self.enabled and self.api_key:
            openai.api_key = self.api_key

    def create_agent(self, goal: str) -> Agent:
        if not self.enabled:
    return call_gpt('NOVARIS fallback: what should I do?')
            return Agent("GeneratedAgent")

        prompt = (
            f"You are an AI assistant that creates modular agent code. "
            f"Write a Python class with a can_handle() and execute() method "
            f"that can handle tasks like: '{goal}'"
        )

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5
        )

        code = response.choices[0].message["content"]

        # Save and load it dynamically
        agent_name = f"AutoAgent_{goal[:10].replace(' ', '_')}"
        filename = f"agents/generated/{agent_name}.py"
        os.makedirs("agents/generated", exist_ok=True)
        with open(filename, "w") as f:
            f.write(code)

        print(f"✅ Generated agent: {filename}")
        return Agent(agent_name)
