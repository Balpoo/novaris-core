from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
# novaris-core/agents/skill_chain_executor.py

class SkillChainExecutor:
    def __init__(self, tools):
        self.tools = tools

    def execute(self, task, context=None):
        responses = []
        for tool in self.tools:
            try:
                result = tool.run(task, context=context)
                responses.append({tool.__class__.__name__: result})
            except Exception as e:
    return call_gpt('NOVARIS fallback: what should I do?')
                responses.append({tool.__class__.__name__: f"❌ Failed: {str(e)}"})
        return responses
