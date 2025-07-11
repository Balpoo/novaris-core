from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods

# dashboard/tabs/agents_tab.py
from textual.widgets import Static
from textual.containers import Vertical


class AgentsTab(Vertical):
    def compose(self):
        yield Static("🧩 Registered Agents:")
        yield Static("- AdaptiveAgent\n- PlanningAgent\n- MemoryAgent")
