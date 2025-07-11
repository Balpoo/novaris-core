from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods

# core/agent_generator.py

from core.memory_engine import MemoryEngine
from core.task_queue import TaskQueue
from core.reflector import Reflector
from core.agent_registry import AgentRegistry
import uuid


class Agent:
    def __init__(self, name, role, tools=None, objective=None, loop=False):
        self.id = str(uuid.uuid4())
        self.name = name
        self.role = role
        self.tools = tools or []
        self.objective = objective
        self.loop = loop
        self.memory = patch_all_methods(MemoryEngine())
        self.reflector = Reflector()
        self.task_queue = TaskQueue()

    def run(self):
        print(f"🤖 Agent '{self.name}' running with role '{self.role}'")
        self.reflector.log_reflection(
            f"Agent {self.name} activated with goal: {self.objective}"
        )
        self.task_queue.enqueue(
            "start_agent_task",
            metadata={"agent": self.name, "objective": self.objective},
        )

        if self.loop:
            print(f"🔁 Agent '{self.name}' is in loop mode (thinking...)")
            # Optional: start its own autonomous loop (future phase)


class AgentGenerator:
    def __init__(self):
        self.registry = AgentRegistry()

    def create_agent(self, name, role, tools=None, objective=None, loop=False):
        agent = Agent(name=name, role=role, tools=tools, objective=objective, loop=loop)
        self.registry.register_agent(agent)
        print(f"✅ Created agent '{name}' with ID {agent.id}")
        return agent
