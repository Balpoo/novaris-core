from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods

# demo_reflection_engine.py

from reflection.reflection_engine import ReflectionEngine
from memory.memory_store import MemoryStore


def run_demo():
    memory = MemoryStore()
    engine = ReflectionEngine(memory)

    while True:
        task = input("🔍 Enter a task to reflect on (or 'exit'): ").strip()
        if task.lower() == "exit":
            break
        reflection = engine.reflect_on_task(task)

        print("\n📋 Reflection Result:")
        for k, v in reflection.items():
            if isinstance(v, list):
                for line in v:
                    print("   ", line)
            else:
                print(f"   {k}: {v}")


if __name__ == "__main__":
    run_demo()
