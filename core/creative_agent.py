from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods

# core/creative_agent.py

from core.memory_engine import MemoryEngine
from core.reflector import Reflector
from core.task_queue import TaskQueue
from core.agent_registry import AgentRegistry

import uuid
import random


class CreativeAgent:
    def __init__(self, name="CreativeSpark", style="neutral", tone="inspirational"):
        self.id = str(uuid.uuid4())
        self.name = name
        self.style = style
        self.tone = tone
        self.memory = patch_all_methods(MemoryEngine())
        self.reflector = Reflector()
        self.task_queue = TaskQueue()
        self.registry = AgentRegistry()
        self.registry.register_agent(self)

    def brainstorm(self, prompt, mode="idea"):
        self.reflector.log_reflection(f"{self.name} received creative prompt: {prompt}")
        base_responses = {
            "idea": [
                f"💡 What if we made '{prompt}' into a 3-part series?",
                f"✨ '{prompt}' could evolve into a seasonal theme collection.",
                f"🎯 Let's turn '{prompt}' into a customer challenge with a reward.",
            ],
            "name": [
                f"🔥 How about 'Nova{random.randint(100,999)}' as a bold name?",
                f"🌀 '{prompt}' → becomes 'EchoVerse' or 'Tradiflux'",
                f"🔮 Inspired by '{prompt}', I suggest 'Mythos Spark'.",
            ],
            "script": [
                f"🎬 Scene 1: You wake up to '{prompt}' and everything changes...",
                f"📜 Narration starts: 'In a world shaped by {prompt}…'",
                f"🎙️ VO: 'Introducing the future of {prompt}, crafted for legends…'",
            ],
        }

        suggestions = base_responses.get(mode, ["⚠️ Unknown creative mode."])
        idea = random.choice(suggestions)
        self.memory.store_thought(f"Generated creative idea for '{prompt}': {idea}")
        return idea

    def run_creative_task(self, task_type, prompt):
        print(f"🎨 CreativeAgent [{self.name}] running task: {task_type} → '{prompt}'")
        result = self.brainstorm(prompt, mode=task_type)
        print(f"🧠 Creative Output: {result}")
        return result
