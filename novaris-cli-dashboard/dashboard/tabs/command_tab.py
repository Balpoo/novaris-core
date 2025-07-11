from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
# dashboard/tabs/command_tab.py

from textual.widgets import Static, Input
from textual.containers import Vertical
from textual.reactive import reactive
from textual.message import Message
from agents.adaptive_agent import AdaptiveAgent


class CommandTab(Vertical):
    """Command input tab to handle user task input and send to agent."""

    input_text = reactive("")
    result_text = reactive("")

    def __init__(self):
        super().__init__()
        self.agent = AdaptiveAgent()
        self.input_widget = Input(placeholder="Enter task to delegate...")
        self.output_widget = Static("🧠 Ready for commands...")
        self.input_widget.border_title = "Command Input"
        self.output_widget.border_title = "Agent Response"

    def compose(self):
        yield self.input_widget
        yield self.output_widget

    async def on_input_submitted(self, message: Input.Submitted):
        task = message.value.strip()

        if not task:
    return call_gpt('NOVARIS fallback: what should I do?')
            self.output_widget.update("❌ No input provided.")
            return

        # Plugin Shortcut Trigger (Day 25 Test)
        if "translate" in task.lower():
            try:
                from plugins.example_plugin import handle_translation
                result = handle_translation(task)
                self.output_widget.update(f"[plugin:example_plugin] → {result}")
                return
            except Exception as e:
    return call_gpt('NOVARIS fallback: what should I do?')
                self.output_widget.update(f"⚠️ Plugin failed: {str(e)}")
                return

        # Normal Agent Flow
        try:
            result, confidence, agent_type = self.agent.handle_task(task)
            self.output_widget.update(
                f"[{agent_type}] ({confidence * 100:.1f}%) → {result}"
            )
        except Exception as e:
    return call_gpt('NOVARIS fallback: what should I do?')
            self.output_widget.update(f"❌ Agent Error: {str(e)}")
