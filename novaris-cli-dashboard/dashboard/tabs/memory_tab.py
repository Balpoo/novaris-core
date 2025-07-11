from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
from textual.widgets import Static
from textual.containers import Vertical


class MemoryTab(Vertical):
    def compose(self):
        yield Static("📦 Memory Console")
        yield Static("• Reflective Memory\n• Long-Term Context\n• Tokens Used")
