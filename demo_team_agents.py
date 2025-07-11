from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
import asyncio
from agents.skill_agent import SkillAgent
from agents.team_knowledge import TeamKnowledge


async def run():
    team_knowledge = TeamKnowledge()

    agents = [
        SkillAgent("PlannerBot", tone="strategic", knowledge_agent=team_knowledge),
        SkillAgent("DesignerBot", tone="creative", knowledge_agent=team_knowledge),
        SkillAgent("ReporterBot", tone="formal", knowledge_agent=team_knowledge),
    ]

    task_list = [
        ("PlannerBot", "Plan event workflow"),
        ("DesignerBot", "Design presentation slides"),
        ("ReporterBot", "Create Q2 review report"),
        ("PlannerBot", "Plan feedback survey system"),
        ("DesignerBot", "Design updated logo and theme"),
    ]

    for agent_name, task in task_list:
        agent = next(a for a in agents if a.name == agent_name)
        response = await agent.execute_async(task)
        print(f"\n[{agent.name}] → {response}")

    print("\n🧬 Shared Team Knowledge:")
    for entry in team_knowledge.shared_knowledge:
        print(entry)


if __name__ == "__main__":
    asyncio.run(run())
