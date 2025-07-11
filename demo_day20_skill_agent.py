from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods

# demo_day20_skill_agent.py

import asyncio
from agents.skill_agent import SkillAgent
from agents.team_knowledge import TeamKnowledge  # ✅ Shared skill memory


async def run():
    # ✅ Create the shared knowledge object
    shared_knowledge = TeamKnowledge()

    # ✅ Inject shared knowledge into agent
    agent = SkillAgent(
        name="SkillBot", tone="proactive", knowledge_agent=shared_knowledge
    )

    tasks = [
        "Plan marketing strategy for Q3",
        "Design customer onboarding journey",
        "Generate Q2 performance report",
        "Plan revenue stream for new product",
        "Fix layout design on homepage",
    ]

    print(f"\n🚀 Starting task run for agent: {agent.name}\n")

    for task in tasks:
        response = await agent.execute_async(task)
        print(response)

    # Print skill summary
    print("\n📊 Final Skill Summary:")
    for skill, score in agent.get_skill_summary().items():
        print(f"→ {skill.title()}: {score} avg")

    # Print profile
    print("\n🧠 Agent Profile:")
    profile = agent.get_profile()
    print(f"Name: {profile['Agent']}")
    print(f"Level: {profile['Level']}")
    print(f"XP: {profile['XP']}")
    for skill, avg_score in profile["Skills"].items():
        print(f"• {skill.title()} → Avg Score: {avg_score}")

    # ✅ View shared memory entries (TeamKnowledge)
    if shared_knowledge.shared_knowledge:
        print("\n🧬 Shared Team Knowledge:")
        for entry in shared_knowledge.shared_knowledge:
            print(entry)


if __name__ == "__main__":
    asyncio.run(run())
