from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods

# core/gpt_dev_day_generator.py

from utils.logs import log


class GPTDevDayGenerator:
    def __init__(self, memory, planner):
        self.memory = memory
        self.planner = planner

    def generate_next_day(self):
        recent = self.memory.query("dev day")
        last_summary = recent[-1] if recent else "Build core planner"

        next_steps = [
            {"task": "Learn Python Networking", "agent": "learning"},
            {"task": "Build File Download Skill", "agent": "utility"},
            {"task": "Understand HTTP APIs", "agent": "network"},
            {"task": "Create Self-Evaluation Agent", "agent": "reflector"},
        ]

        log(f"GPT Generator Suggests: {[task['task'] for task in next_steps]}")
        return next_steps


if __name__ == "__main__":

    class DummyMemory:
        def query(self, tag):
            return ["Dev Day 56: Build dynamic memory engine"]

    class DummyPlanner:
        pass

    generator = GPTDevDayGenerator(DummyMemory(), DummyPlanner())
    tasks = generator.generate_next_day()
    print("Generated Tasks:", tasks)
    assert isinstance(tasks, list) and len(tasks) > 0
    assert all("task" in t and "agent" in t for t in tasks)
