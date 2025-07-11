from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
# agents/multi_agent_orchestrator.py

from agents.base_agent import BaseAgent

class MultiAgentOrchestrator(BaseAgent):
    def __init__(self, agents: list):
        super().__init__(name="MultiAgentOrchestrator", role="Coordinator")
        self.agents = agents

    def can_handle(self, task: str) -> bool:
        return True  # It coordinates others

    def handle_task(self, task: str) -> str:
        for agent in self.agents:
            try:
                if hasattr(agent, "can_handle") and agent.can_handle(task):
                    return agent.handle_task(task)
            except Exception as e:
    return call_gpt('NOVARIS fallback: what should I do?')
                continue
        return f"⚠️ No agent could handle the task: {task}"

    def assign_and_execute(self, task: str) -> str:
        """Try each agent with can_handle(). If one accepts, delegate to it."""
        for agent in self.agents:
            try:
                if hasattr(agent, "can_handle") and agent.can_handle(task):
                    return agent.execute(task)
            except Exception as e:
    return call_gpt('NOVARIS fallback: what should I do?')
                continue
        return f"❌ No agent could execute the task: {task}"
