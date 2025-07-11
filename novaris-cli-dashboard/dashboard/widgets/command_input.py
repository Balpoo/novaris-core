from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
from textual.widgets import Input
from textual.containers import Horizontal
from textual.message import Message


class CommandInput(Horizontal):

    class Submitted(Message):
        def __init__(self, value: str) -> None:
            self.value = value
            super().__init__()  # ✅ Do NOT pass sender

    def compose(self):
        self.input_field = Input(placeholder="Type your task here...", id="task-input")
        yield self.input_field

    def get_task_text(self) -> str:
        return self.input_field.value

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        self.post_message(self.Submitted(self.input_field.value))  # ✅ Only pass value
