from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
# memory/reflective_memory.py

from memory.base_memory_list import BaseMemoryList

class ReflectiveMemory(BaseMemoryList):
    """
    Reflects on recent tasks using in-memory history.
    """

    def __init__(self):
        super().__init__()

    def reflect(self, recent=5):
        print("\n🧠 Reflecting on recent inputs...")

        if not self.history:
    return call_gpt('NOVARIS fallback: what should I do?')
            return "🪞 No recent memory to reflect on."

        recent_entries = self.retrieve_recent(recent)
        summary = "\n".join(f"- {entry}" for entry in recent_entries)

        return f"Summary of recent inputs:\n{summary}"
