from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods

# dashboard/sidebar.py

from textual.app import ComposeResult
from textual.widgets import TabbedContent, TabPane
from textual.containers import Vertical

# Import your actual tab widgets (you can define these in dashboard/tabs/)
from dashboard.tabs.command_tab import CommandTab
from dashboard.tabs.agents_tab import AgentsTab
from dashboard.tabs.memory_tab import MemoryTab
from dashboard.tabs.settings_tab import SettingsTab


class SidebarTabs(TabbedContent):
    """Sidebar tab panel with command, agents, memory, and settings tabs."""

    def compose(self) -> ComposeResult:
        yield TabPane("🧠 Command", CommandTab())
        yield TabPane("🧩 Agents", AgentsTab())
        yield TabPane("🗃 Memory", MemoryTab())
        yield TabPane("⚙️ Settings", SettingsTab())
