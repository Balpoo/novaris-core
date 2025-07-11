from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
from agents.agent_base import Agent


class StrategyAgent(Agent):
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)
        self.current_strategy = "default"
        self.self_coaching_log = []

    async def execute_async(self, task: str) -> str:
        result = await super().execute_async(task)

        # Reflect and adjust if needed
        if "fail" in result.lower() or "retry" in result.lower():
            self.self_coach(task, result)
            self.rewrite_strategy("fail_pattern")

        return result

    def self_coach(self, task: str, result: str):
        msg = f"🔍 Detected poor result on task '{task}'. Consider rephrasing, escalating, or delaying similar tasks."
        self.self_coaching_log.append(msg)
        self.memory.remember(
            task="self_coach", result=msg, agent_name=self.name, entry_type="thought"
        )

    def rewrite_strategy(self, trigger: str):
        if trigger == "fail_pattern":
            self.current_strategy = "retry_with_context"
            msg = f"🛠️ Strategy updated to: {self.current_strategy} due to recent failures."
            self.self_coaching_log.append(msg)
            self.memory.remember(
                task="strategy_update",
                result=msg,
                agent_name=self.name,
                entry_type="thought",
            )

    def get_self_coaching_log(self):
        return self.self_coaching_log
