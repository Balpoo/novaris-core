from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
import asyncio
from agents.agent_base import Agent


class ParentAgent(Agent):
    def can_handle(self, task: str) -> bool:
        return "strategy" in task.lower()


class ChildAgent(Agent):
    def can_handle(self, task: str) -> bool:
        return "design" in task.lower()


async def run_demo():
    # Setup agents
    parent = ParentAgent(name="PlanningAgent", role="Planner", tone="strategic")
    child = ChildAgent(name="DesignAgent", role="UX Designer", tone="creative")

    # Link agents
    parent.add_child(child)

    # Child receives and remembers a task
    design_task = "Create wireframes for the mobile app"
    print(await child.execute_async(design_task))

    # Child shares a thought to parent
    child.propagate_thought(
        "Need clarity on user flow before continuing", direction="up"
    )

    # Parent shares a suggestion to child
    parent.propagate_thought("Refer to the client’s approved sitemap", direction="down")

    # Parent receives its own task
    strategy_task = "Plan launch strategy for Q4"
    print(await parent.execute_async(strategy_task))

    # Show memory of each agent
    print("\n🧠 MEMORY LOGS")
    for agent in [parent, child]:
        print(f"\n📒 {agent.name}'s Memory:")
        for entry in agent.get_memory():
            print(f"  [{entry['timestamp']}] ({entry['type']}): {entry['content']}")


# Run the demo
if __name__ == "__main__":
    asyncio.run(run_demo())
