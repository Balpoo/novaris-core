from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods

# core/agent_collaborator.py

from core.executor_agent import ExecutorAgent
from core.reflection_engine import log_execution_result
from core.trust_manager import TrustManager


class AgentCollaborator:
    def __init__(self):
        self.executor = patch_all_methods(ExecutorAgent())
        self.trust = TrustManager()

    def assign_task(self, task: dict) -> dict:
        max_retries = 2
        attempt = 0
        result = None

        while attempt <= max_retries:
            print(f"🔁 Attempt {attempt + 1} for task: {task['type']}")
            result = self.executor.perform_task(task)

            # Log and update trust
            log_execution_result(task, result)
            self.trust.update_trust_score(
                "executor", task["type"], result["status"] == "success"
            )

            if result["status"] == "success":
                break
            attempt += 1

        return result
