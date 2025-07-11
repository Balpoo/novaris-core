from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
import datetime
from core.memory_engine import MemoryEngine


class Reflector:
    def __init__(self):
        self.memory = patch_all_methods(MemoryEngine())

    def log_reflection(self, message: str):
        timestamp = datetime.datetime.now().isoformat()
        entry = {
            "summary": message,
            "source": "reflection",
            "metadata": {"timestamp": timestamp},
        }
        self.memory.add_thought(**entry)
        print(f"[Reflection] {message}")

    def reflect_on_task(
        self, task: str, result: str, agent: str = "unknown", confidence: float = 1.0
    ):
        """Store reflections and performance from completed tasks."""
        summary = f"Task: {task[:80]}\nResult: {result[:80]}\nAgent: {agent}\nConfidence: {confidence:.2f}"
        self.memory.add_thought(
            summary=summary,
            source="reflection",
            metadata={
                "agent": agent,
                "task": task,
                "result": result,
                "confidence": confidence,
                "timestamp": datetime.datetime.utcnow().isoformat(),
            },
        )
        print(f"🪞 Reflection stored for: {task[:50]}...")

    def reflect_on_failure(self, task: str, reason: str, agent: str = "unknown"):
        """Log failed attempts for improvement."""
        summary = f"FAILED Task: {task[:80]}\nReason: {reason}"
        self.memory.add_thought(
            summary=summary,
            source="failure",
            metadata={
                "agent": agent,
                "failure_reason": reason,
                "task": task,
                "timestamp": datetime.datetime.utcnow().isoformat(),
            },
        )
        print(f"❌ Failure reflection stored for: {task[:50]}...")
