from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
import asyncio
import random
from agents.persona import AgentPersona
from memory.agent_memory import AgentMemory


class Agent:
    def __init__(
        self,
        name,
        role="Assistant",
        tone="neutral",
        voice_id=None,
        description=None,
        knowledge_agent=None,
    ):
        self.name = name
        self.description = description or f"{name} - general purpose agent"
        self.persona = AgentPersona(name, role, tone, voice_id)
        self.memory = AgentMemory()
        self.knowledge_agent = knowledge_agent  # Optional knowledge store
        self.parent = None
        self.children = []

    def set_parent(self, parent_agent):
        self.parent = parent_agent

    def add_child(self, child_agent):
        child_agent.set_parent(self)
        self.children.append(child_agent)

    def remember(self, task: str, result: str, entry_type: str = "task"):
        self.memory.remember(
            task=task, result=result, agent_name=self.name, entry_type=entry_type
        )

    def get_memory(self, filter_by_type: str = None):
        return self.memory.get_memory(
            agent_name=self.name, filter_by_type=filter_by_type
        )

    def propagate_thought(self, message: str, direction: str = "up"):
        """Share a thought with parent or children."""
        if direction == "up" and self.parent:
            self.parent.receive_thought(message, from_agent=self)
        elif direction == "down":
            for child in self.children:
                child.receive_thought(message, from_agent=self)

    def receive_thought(self, message: str, from_agent):
        log = f"Thought received from {from_agent.name}: {message}"
        self.remember(task="received_thought", result=log, entry_type="thought")

    def can_handle(self, task: str) -> bool:
        """Override in subclasses."""
        return False

    def execute(self, task: str) -> str:
        """Sync fallback."""
        self.persona.adjust_emotion(task)
        response = f"{self.name} says: I can't handle that yet."
        self.remember(task, response)
        return self._styled_response(response)

    async def execute_async(self, task: str) -> str:
        """Primary async execution."""
        print(f"🚀 [{self.name}] Executing task: {task}")
        await asyncio.sleep(random.uniform(0.5, 1.2))  # Simulate async execution

        # 🧠 Check for override
        override = self.scan_for_override()
        if override:
            print(f"⚡ Executing OVERRIDE command for {self.name}: {override}")
            self.remember(
                task="override_executed", result=override, entry_type="action"
            )
            return self._styled_response(f"[OVERRIDE] {override}")

        if self.knowledge_agent and any(
            k in task.lower() for k in ["vision", "mission", "financial", "data"]
        ):
            results = self.knowledge_agent.query(task)
            result = f"[{self.name}] Knowledge-based result: {results}"
        else:
            result = f"[{self.name}] completed: {task}"

        self.remember(task, result)
        self.persona.adjust_emotion(result)
        return self._styled_response(result)

    async def fallback_async(self) -> str:
        print(f"🛟 [{self.name}] Running fallback...")
        await asyncio.sleep(0.5)
        fallback_response = f"[{self.name}] fallback result used."
        self.remember("fallback", fallback_response)
        return self._styled_response(fallback_response)

    def scan_for_override(self) -> str:
        """Scan agent memory for the latest override command and return it."""
        overrides = self.memory.get_memory(self.name, filter_by_type="thought")
        for entry in reversed(overrides):
            if entry["task"] == "override_command":
                return entry["content"]
        return ""

    def _styled_response(self, response: str) -> str:
        return f"[{self.name} • {self.persona.tone} • {self.persona.emotion_state}] → {response}"
