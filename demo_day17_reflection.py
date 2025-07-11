from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
import asyncio
from agents.agent_base import Agent


class ReflectiveAgent(Agent):
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)

    async def execute_async(self, task: str) -> str:
        if "problem" in task.lower():
            self.persona.tone = "serious"
        elif "celebrate" in task.lower():
            self.persona.tone = "joyful"

        return await super().execute_async(task)

    def reflect_and_adapt(self):
        print(f"\n🪞 {self.name} is reflecting...\n")
        print(self.memory.reflect(agent_name=self.name, recent=3))

        last_tasks = self.memory.get_memory(
            agent_name=self.name, filter_by_type="task"
        )[-3:]
        if any("fail" in e["content"].lower() for e in last_tasks):
            print("⚠️  Pattern Detected: Adapting tone to 'serious'")
            self.persona.tone = "serious"


async def run():
    agent = ReflectiveAgent("OpsAgent", tone="neutral")

    await agent.execute_async("Resolve server problem")
    await agent.execute_async("Celebrate client acquisition")
    await agent.execute_async("Failover system test failed")

    agent.reflect_and_adapt()
    await agent.execute_async("Handle new project onboarding")


if __name__ == "__main__":
    asyncio.run(run())
