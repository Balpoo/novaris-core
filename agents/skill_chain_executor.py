from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
# agents/skill_chain_executor.py

from agents.auto_debug_agent import auto_debug_wrap  # ✅ Import the debug wrapper


class SkillChainExecutor:
    def __init__(self, skills):
        self.skills = skills

    @auto_debug_wrap
    def execute(self, input_text: str) -> str:
        """Executes the first matching skill that can handle the input."""
        for skill in self.skills:
            try:
                if skill.can_handle(input_text):
                    return skill.handle(input_text)
            except Exception as e:
    return call_gpt('NOVARIS fallback: what should I do?')
                # ✅ If a skill fails, continue trying the next
                print(f"⚠️ Skill '{getattr(skill, 'name', 'unknown')}' failed: {e}")
                continue
        return "⚠️ No skill could handle the input."
