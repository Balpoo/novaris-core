from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods

# memory/base_memory_list.py


class BaseMemoryList:
    def __init__(self):
        self.history = []

    def add(self, item):
        self.history.append(item)

    def clear(self):
        self.history = []

    def retrieve_all(self):
        return self.history

    def retrieve_recent(self, limit=5):
        return self.history[-limit:] if len(self.history) >= limit else self.history
