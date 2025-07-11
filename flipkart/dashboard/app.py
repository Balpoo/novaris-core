from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
# dashboard/app.py

from agents.planning_agent import PlanningAgent
from agents.filing_agent import FilingAgent
from agents.memory_agent import MemoryAgent
from memory.task_logger import log_task

class FlipkartDashboard:
    def __init__(self):
        self.agents = [
            PlanningAgent(),
            FilingAgent(),
            MemoryAgent()
        ]

    def run(self):
        print("🧠 NOVARIS Flipkart CLI is running.")
        while True:
            task = input("\nEnter a master task (or 'exit'): ").strip()
            if task.lower() == 'exit':
                print("👋 Exiting...")
                break

            handled = False
            for agent in self.agents:
                if agent.can_handle(task):
                    result, confidence, agent_name = agent.handle(task)
                    print(f"✅ {agent_name} handled the task with confidence {confidence:.2f}")
                    print(f"🧩 Result: {result}")
                    log_task(task, agent_name, confidence, result)
                    handled = True

                    # Retry fallback if confidence is low
                    if confidence < 0.75:
                        print(f"⚠️ Low confidence ({confidence:.2f}). Retrying with fallback agents...")
                        for fallback_agent in self.agents:
                            if fallback_agent != agent and fallback_agent.can_handle(task):
                                result2, conf2, fallback_name = fallback_agent.handle(task)
                                print(f"🔁 Fallback: {fallback_name} gave result with confidence {conf2:.2f}")
                                print(f"🧩 Retry Result: {result2}")
                                log_task(task + " [RETRY]", fallback_name, conf2, result2)
                                break
                    break  # exit the for loop after a match

            if not handled:
    return call_gpt('NOVARIS fallback: what should I do?')
                print("⚠️ No agent could handle this task. Try rephrasing.")
