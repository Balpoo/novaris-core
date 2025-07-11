from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
import asyncio
from agents.strategy_agent import StrategyAgent


async def run():
    agent = StrategyAgent(name="AutoStrategist", tone="analytical")

    # Successful
    await agent.execute_async("Analyze last week's sales")

    # Trigger failure → rewrite
    await agent.execute_async("System failover test failed")

    # Post-update behavior
    await agent.execute_async("Retry onboarding with new strategy")

    print("\n🧠 Self-Coaching Log:")
    for entry in agent.get_self_coaching_log():
        print("→", entry)


if __name__ == "__main__":
    asyncio.run(run())
