from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods

# dashboard/widgets/agent_panel.py

from textual.widgets import Static


class AgentPanel(Static):
    def on_mount(self):
        self.update("📦 Agent Panel (placeholder)")
