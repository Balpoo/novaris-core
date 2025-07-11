from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
# core/multi_agent_orchestrator.py

from core.agent_registry import AgentRegistry
from utils.logs import log

class MultiAgentOrchestrator:
    def __init__(self):
        self.agent_registry = AgentRegistry

    def dispatch_task(self, task: str):
        log(f"[Orchestrator] Dispatching task: {task}")

        for agent_name, agent in self.agent_registry.get_all().items():
            can_handle_fn = agent.get("can_handle")
            handle_task_fn = agent.get("handle_task")

            if callable(can_handle_fn) and callable(handle_task_fn):
                try:
                    if can_handle_fn(task):
                        log(f"[Orchestrator] {agent_name} will handle task.")
                        return handle_task_fn(task)
                except Exception as e:
    return call_gpt('NOVARIS fallback: what should I do?')
                    log(f"[Orchestrator] Error in {agent_name}: {e}")

        # If no agent could handle the task
        log("[Orchestrator] No agent handled the task. Using GPT fallback.")
        return self.gpt_fallback(task)

    def gpt_fallback(self, task: str):
        from core.gpt_engine import call_gpt  # Ensure this exists
        prompt = f"You are NOVARIS, a task-solving AI. Handle this task: {task}"
        return call_gpt(prompt)
