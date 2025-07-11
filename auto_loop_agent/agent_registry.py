from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods

# agents/agent_registry.py

from agents.base_agent import Agent
from agents.knowledge_agent import KnowledgeAgent


class AgentRegistry:
    def __init__(self, knowledge_agent: KnowledgeAgent = None):
        self.knowledge_agent = knowledge_agent

        # 🎯 Register specialized agents with persona + knowledge access
        self.agent_map = {
            "cater": Agent(
                name="CateringAgent",
                role="Vendor Manager",
                tone="friendly",
                description="Handles catering bookings",
            ),
            "decor": Agent(
                name="DecorAgent",
                role="Event Designer",
                tone="aesthetic",
                description="Handles decor planning",
            ),
            "vision": Agent(
                name="VisionAgent",
                role="Strategist",
                tone="thoughtful",
                voice_id="v1",
                description="Handles company vision tasks",
                knowledge_agent=self.knowledge_agent,
            ),
            "financials": Agent(
                name="FinanceAgent",
                role="Financial Analyst",
                tone="analytical",
                voice_id="v2",
                description="Handles financial insights",
                knowledge_agent=self.knowledge_agent,
            ),
        }

    def get_agent_for(self, task_desc: str) -> Agent:
        """
        Match a task description to the most appropriate agent.
        Falls back to a dynamically created generic agent.
        """
        task_desc_lower = task_desc.lower()
        for keyword, agent in self.agent_map.items():
            if keyword in task_desc_lower:
                print(f"🔍 Matched agent [{agent.name}] for task: {task_desc}")
                return agent

        print(f"🧠 Spawning fallback agent for unknown task: {task_desc}")
        return self.spawn_generic_agent(task_desc)

    def spawn_generic_agent(self, task_desc: str) -> Agent:
        return Agent(
            name="GenericAgent",
            role="General Assistant",
            tone="neutral",
            description=f"Auto-spawned for: {task_desc}",
            knowledge_agent=self.knowledge_agent,
        )
