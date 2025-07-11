from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
from textual.scroll_view import ScrollView
from textual.widgets import Static
from rich.text import Text
from datetime import datetime


class MemoryLog(ScrollView):
    def __init__(self):
        super().__init__()
        self.border_title = "Memory"
        self.border_subtitle = "Log"
        self.log_box = Static()
        self.call_after_refresh(self._mount_log_box)

    def _mount_log_box(self):
        self.mount(self.log_box)

    def log_message(self, message: str):
        timestamp = datetime.now().strftime("[%I:%M %p]")  # e.g., [12:44 PM]

        # Detect message type
        if "[USER]" in message:
            color = "cyan"
        elif "[AGENT]" in message:
            color = "green"
        elif "[!]" in message or "[ERROR]" in message:
            color = "red"
        else:
            color = "white"

        # Build new line
        new_line = Text(f"{timestamp} {message}", style=color)

        # Append to existing
        current = self.log_box.renderable or Text()
        if isinstance(current, str):
            current = Text(current)
        current.append(new_line.append("\n"))
        self.log_box.update(current)

        # Auto-scroll to bottom
        self.scroll_end(animate=False)
