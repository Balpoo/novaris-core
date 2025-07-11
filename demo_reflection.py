from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods

# demo_reflection.py

from memory.reflective_memory import ReflectiveMemory


def run_demo():
    mem = ReflectiveMemory()

    mem.add("Plan product roadmap")
    mem.add("Fix login bug")
    mem.add("Write onboarding guide")
    mem.add("Research market trends")
    mem.add("Schedule client call")

    print(mem.reflect(recent=5))


if __name__ == "__main__":
    run_demo()
