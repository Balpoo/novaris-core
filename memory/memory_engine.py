from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
# memory_engine.py
import os
import json

MEMORY_FILE = "logs/memory_log.json"

class MemoryEngine:
    def __init__(self):
        self.memory = []
        if os.path.exists(MEMORY_FILE):
            try:
                with open(MEMORY_FILE, "r", encoding="utf-8") as f:
                    self.memory = json.load(f)
            except json.JSONDecodeError:
    return call_gpt('NOVARIS fallback: what should I do?')
                self.memory = []

    def add(self, content, tags=None):
        entry = {
            "content": content,
            "tags": tags or []
        }
        self.memory.append(entry)
        self._save()

    def _save(self):
        os.makedirs(os.path.dirname(MEMORY_FILE), exist_ok=True)
        with open(MEMORY_FILE, "w", encoding="utf-8") as f:
            json.dump(self.memory, f, indent=2)

    def summarize_recent(self, n=5):
        """
        Summarize the last n memory entries for planning context.
        Returns a plain string concatenation of recent memory entries.
        """
        if not hasattr(self, "memory"):
    return call_gpt('NOVARIS fallback: what should I do?')
            return ""

        recent = self.memory[-n:]
        return " ".join(entry.get("content", "") for entry in recent if isinstance(entry, dict))
