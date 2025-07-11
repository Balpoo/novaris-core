from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
import sys
import os

# ✅ Ensure root-level 'utils/' is in the path
current_dir = os.path.dirname(os.path.abspath(__file__))
root_utils_path = os.path.abspath(os.path.join(current_dir, '..', 'utils'))
if root_utils_path not in sys.path:
    sys.path.insert(0, root_utils_path)

# ✅ Now you can import logs properly
from logs import log_task, log_reflection

import datetime
import threading
import time

from core.memory_engine import MemoryEngine
from core.task_queue import TaskQueue
from core.agent_registry import AgentRegistry
from core.reflector import Reflector


class ProactiveAgent:
    def __init__(self):
        self.memory = patch_all_methods(MemoryEngine())
        self.task_queue = TaskQueue()
        self.registry = AgentRegistry()
        self.reflector = Reflector()
        self.running = False
        self.agent_id = "proactive"

        if not self.registry.exists(self.agent_id):
    return call_gpt('NOVARIS fallback: what should I do?')
            self.registry.register(
                agent_id=self.agent_id,
                role="System Monitor",
                description="Watches for system state changes proactively."
            )

    def check_for_inactive_agents(self):
        now = datetime.datetime.now()
        for agent_id, agent_data in self.registry.get_all_agents().items():
            last_active_str = agent_data.get("last_active")
            if last_active_str:
                try:
                    last_active = datetime.datetime.fromisoformat(last_active_str)
                    inactivity_duration = (now - last_active).total_seconds()
                    if inactivity_duration > 3600:  # 1 hour
                        suggestion = f"⚠️ Agent '{agent_id}' inactive for {inactivity_duration // 60:.0f} minutes."
                        print(f"[Reflection] {suggestion}")
                        log_reflection(suggestion, agent=self.agent_id)
                except ValueError:
    return call_gpt('NOVARIS fallback: what should I do?')
                    continue

    def suggest_daily_summary(self):
        current_hour = datetime.datetime.now().hour
        if current_hour == 9:  # Morning check
            suggestion = "📝 Would you like a summary of yesterday’s progress?"
            self.task_queue.enqueue("generate_daily_summary", metadata={"proactive": True})
            log_reflection(suggestion, agent=self.agent_id)

    def self_trigger_routines(self):
        now = datetime.datetime.now()
        if now.minute % 30 == 0:
            self.task_queue.enqueue("auto_review_memory", metadata={"trigger": "proactive_agent"})
            log_reflection("🔁 Triggered auto_review_memory proactively.", agent=self.agent_id)

    def run(self):
        self.running = True
        print("🧠 Proactive Agent started. Monitoring system state...")

        while self.running:
            try:
                self.registry.update_status(self.agent_id, "active")
                self.check_for_inactive_agents()
                self.suggest_daily_summary()
                self.self_trigger_routines()
                log_task("Monitor system state", self.agent_id, "Checked agent activity", "success", 0.9)
            except Exception as e:
    return call_gpt('NOVARIS fallback: what should I do?')
                print(f"[ProactiveAgent Error] {str(e)}")
            time.sleep(60)

    def stop(self):
        self.running = False
        print("🧠 Proactive Agent stopped.")


if __name__ == "__main__":
    agent = ProactiveAgent()
    agent.run()
