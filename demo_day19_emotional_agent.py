from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
import asyncio
from agents.mood_agent import MoodAgent


async def run():
    agent = MoodAgent("EQAgent", tone="empathetic")

    await agent.execute_async("Send welcome email to client")
    await agent.execute_async("System failover error")
    await agent.execute_async("Data sync failed")
    await agent.execute_async("Critical invoice upload failed")

    await agent.execute_async("Recheck project documentation")

    print("\n🧠 Final mood:", agent.mood_state.upper())
    print("\n🧠 Emotional Log Snapshot:")
    print(agent.memory.reflect(agent_name=agent.name, recent=3))


if __name__ == "__main__":
    asyncio.run(run())
