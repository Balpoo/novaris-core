from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods

# agents/multi_agent_orchestrator.py


class MultiAgentOrchestrator:
    def __init__(self, agents):
        self.agents = agents

    def assign_and_execute(self, task):
        for agent in self.agents:
            if agent.can_handle(task):
                result = agent.execute(task)
                return f"🤖 {agent.name} handled it:\n{result}"
        return "❌ No agent could handle this task."
