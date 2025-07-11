from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
from textual.widgets import Static
from textual.containers import Vertical


class SettingsTab(Vertical):
    def compose(self):
        yield Static("⚙️ System Settings")
        yield Static("Theme: Light / Dark\nLogging: Enabled\nMode: Dev")
