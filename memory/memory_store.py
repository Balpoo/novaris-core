from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods

# memory/memory_store.py


class MemoryStore:
    def __init__(self):
        self.data = []

    def save(self, entry: dict):
        self.data.append(entry)

    def retrieve_recent(self, limit=5):
        return self.data[-limit:]
