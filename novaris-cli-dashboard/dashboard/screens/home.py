from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods

# dashboard/screens/home.py

from textual.screen import Screen
from textual.widgets import Static, Button
from textual.containers import Vertical
from dashboard.widgets.command_input import CommandInput
from dashboard.widgets.agent_panel import AgentPanel
from dashboard.widgets.memory_log import MemoryLog

# Optional: Enable real AdaptiveAgent logic
# from agents.adaptive_agent import AdaptiveAgent


class HomeScreen(Screen):
    def __init__(self):
        super().__init__()
        self.agent_panel = AgentPanel()
        self.command_input = CommandInput()
        self.memory_log = MemoryLog()

        # Use real agent if available
        # self.agent = AdaptiveAgent()

    def compose(self):
        """Compose the layout with all main widgets."""
        yield Static("🤖 Welcome to NOVARIS 2.0 Command Center", classes="title")
        yield Vertical(self.agent_panel, self.memory_log, id="top-section")
        yield self.command_input
        yield Button(label="Run Task", id="run-btn", variant="success")

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button click for Run Task."""
        if event.button.id == "run-btn":
            await self.process_task()

    async def on_command_input_submitted(self, message: CommandInput.Submitted) -> None:
        """Handle Enter key submission in CommandInput."""
        await self.process_task()

    async def process_task(self):
        """Central logic for processing tasks and logging results."""
        task = self.command_input.get_task_text().strip()
        if task:
            self.memory_log.log_message(f"[USER] {task}")

            # --- Uncomment to use real agent ---
            # result, confidence, agent_type = self.agent.handle_task(task)
            # response = f"[{agent_type.upper()} | {confidence:.2f}] → {result}"

            # Simulated agent fallback
            response = self.fake_agent_run(task)

            self.memory_log.log_message(f"[AGENT] {response}")
        else:
            self.memory_log.log_message("[!] Please enter a task.")

    def fake_agent_run(self, task: str) -> str:
        """Simulated agent response for demo/testing."""
        return f"Simulated response for: '{task}'"
