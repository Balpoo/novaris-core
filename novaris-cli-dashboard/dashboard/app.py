from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods

# dashboard/app.py

from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual.widgets import Static

from dashboard.sidebar import SidebarTabs
from agents.adaptive_agent import AdaptiveAgent


class NovarisDashboard(App):
    """Main dashboard interface for NOVARIS."""

    CSS_PATH = "styles.css"

    BINDINGS = [("q", "quit", "Quit")]

    def __init__(self):
        super().__init__()
        self.agent = AdaptiveAgent()
        self.last_result = "No tasks yet."

    def compose(self) -> ComposeResult:
        yield Horizontal(
            SidebarTabs(),
            Static(self.last_result, id="result-box", classes="result"),
        )

    def on_mount(self):
        self.query_one("#result-box", Static).update(
            "🧠 NOVARIS loaded. Awaiting command..."
        )

    def update_result(self, message: str):
        """Update the result display box."""
        self.query_one("#result-box", Static).update(message)
