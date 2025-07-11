from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods

# agents/task_executor.py

from agents.adaptive_agent import AdaptiveAgent


class TaskExecutor:
    def __init__(self):
        self.agent = AdaptiveAgent()
        self.history = []

    def execute_all(self, tasks: list):
        print("\n🚀 Executing Multi-Step Plan...\n")
        for i, task in enumerate(tasks, 1):
            print(f"🔹 Step {i}: {task}")
            result, confidence, agent_used = self.agent.handle_task(task)
            print(f"   → [{agent_used}] ({confidence*100:.1f}%) {result}\n")
            self.history.append((task, result, confidence, agent_used))
