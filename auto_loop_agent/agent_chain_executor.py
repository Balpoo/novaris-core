from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods

# agents/agent_chain_executor.py


class AgentChainExecutor:
    def __init__(self, orchestrator):
        self.orchestrator = orchestrator

    def execute_chain(self, tasks):
        results = []
        for task in tasks:
            result = self.orchestrator.assign_and_execute(task)
            results.append((task, result))
        return results
