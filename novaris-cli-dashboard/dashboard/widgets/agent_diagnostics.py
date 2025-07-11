from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods

# dashboard/widgets/agent_diagnostics.py

from textual.widgets import Static


class AgentDiagnostics(Static):
    def __init__(self):
        super().__init__()
        self.update("Diagnostics: Awaiting task...")

    def update_log(self, log: str):
        self.update(f"Diagnostics:\n{log}")
