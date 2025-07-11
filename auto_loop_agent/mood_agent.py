from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
from agents.agent_base import Agent


class MoodAgent(Agent):
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)
        self.mood_state = "stable"  # stable | anxious | overwhelmed

    async def execute_async(self, task: str) -> str:
        result = await super().execute_async(task)

        # Mood update based on task results
        self._update_mood(task, result)
        self._log_emotional_state(task)

        if self.mood_state == "overwhelmed":
            result += " 😰 [Note: I'm currently overwhelmed.]"
        elif self.mood_state == "anxious":
            result += " 😟 [Note: I'm feeling anxious about recent tasks.]"

        return result

    def _update_mood(self, task, result):
        recent = self.memory.get_memory(self.name, filter_by_type="task")[-5:]
        fail_count = sum("fail" in e["content"].lower() for e in recent)

        if self.mood_state == "overwhelmed":
            self.persona.tone = "urgent"
        elif self.mood_state == "anxious":
            self.persona.tone = "cautious"
        else:
            self.persona.tone = "calm"

    def _log_emotional_state(self, task):
        mood_msg = f"❤️ Mood is now: {self.mood_state.upper()} after '{task}'"
        self.memory.remember(
            task="mood_update",
            result=mood_msg,
            agent_name=self.name,
            entry_type="thought",
        )
