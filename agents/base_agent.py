from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods

# agents/base_agent.py


class BaseAgent:
    def __init__(
        self, name: str = None, role: str = "Generalist", tone: str = "neutral"
    ):
        self.name = name or self.__class__.__name__
        self.role = role
        self.tone = tone
        self.memory = type(
            "MemoryMock", (), {"entries": [], "remember": lambda self, t, r: None}
        )()
        self.persona = type(
            "PersonaMock", (), {"adjust_emotion": lambda self, e: None}
        )()

    def can_handle(self, task: str) -> bool:
        return False

    def handle_task(self, task: str) -> str:
        return f"⚠️ {self.name} does not know how to handle this task."

    def _styled_response(self, text: str) -> str:
        return f"[{self.name}]: {text}"

    execute = handle_task  # alias
