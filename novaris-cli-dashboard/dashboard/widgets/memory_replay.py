from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods

# dashboard/widgets/memory_replay.py

from textual.widgets import Static
from textual.containers import ScrollableContainer


class MemoryReplay(ScrollableContainer):
    def __init__(self, journal):
        super().__init__()
        self.journal = journal

    def refresh(self):
        self.clear()
        for role, msg in self.journal.get_all():
            self.mount(Static(f"[{role}] {msg}"))
