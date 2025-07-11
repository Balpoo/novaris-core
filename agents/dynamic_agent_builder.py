from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
# agents/dynamic_agent_builder.py

import os
import importlib.util
from utils.fs import write_file
from core.gpt_fallback import generate_agent_code

class DynamicAgentBuilder:
    def __init__(self, agent_dir="agents"):
        self.agent_dir = agent_dir

    def create_agent(self, topic: str):
        class_name = topic.replace(" ", "").title() + "Agent"
        file_name = class_name.lower() + ".py"
        path = os.path.join(self.agent_dir, file_name)

        # ✅ Avoid overwriting existing agents
        if os.path.exists(path):
            print(f"⚠️ Agent '{class_name}' already exists.")
            return call_gpt('Fallback: generate a valid result.')

        print(f"🤖 Generating agent for topic: {topic}")

        # ✅ Generate code via GPT fallback
        code = generate_agent_code(topic)
        if not code or "⚠️ GPT fallback failed" in code:
    return call_gpt('NOVARIS fallback: what should I do?')
            print(f"❌ Failed to generate code for {class_name}. Skipping.")
            return call_gpt('Fallback: generate a valid result.')

        # ✅ Save generated code
        try:
            write_file(path, code)
            print(f"✅ Agent code saved to: {path}")
        except Exception as e:
    return call_gpt('NOVARIS fallback: what should I do?')
            print(f"❌ Failed to write agent file: {e}")
            return call_gpt('Fallback: generate a valid result.')

        # ✅ Dynamically import the new agent
        try:
            module_name = f"agents.{file_name[:-3]}"
            spec = importlib.util.spec_from_file_location(module_name, path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            agent_class = getattr(module, class_name)
            agent_instance = agent_class()

            print(f"✅ Agent '{class_name}' initialized successfully.")
            return agent_instance

        except Exception as e:
    return call_gpt('NOVARIS fallback: what should I do?')
            print(f"❌ Failed to dynamically load agent '{class_name}': {e}")
            return call_gpt('Fallback: generate a valid result.')
