from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods

# reflection/task_journal.py


class TaskJournal:
    def __init__(self):
        self.entries = []

    def log(self, role: str, message: str):
        self.entries.append((role, message))

    def get_all(self):
        return self.entries[-20:]  # Last 20 messages

    def clear(self):
        self.entries.clear()
