from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.api.config_loader import load_config
from backend.agents.skill_loader import load_skills
from backend.agents.memory_agent import Memory

config = load_config()
skills = load_skills()
memory = Memory()

print("NOVARIS Core Booted ✅")
print("Loaded Skills:", list(skills.keys()))
print()

while True:
    user_input = input("You > ")
    memory.add(user_input)
    matches = memory.query(user_input)
    print("🔍 Memory Matches:", matches)

    if user_input.lower() in ["exit", "quit"]:
        break
