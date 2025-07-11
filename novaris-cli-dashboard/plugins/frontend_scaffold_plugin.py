from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods


class PluginAgent:
    def can_handle(self, task: str) -> bool:
        return "scaffold frontend" in task.lower() or "react" in task.lower()

    def handle(self, task: str) -> tuple:
        return (
            "🖼 Frontend Scaffold:\n"
            "- React + Vite + TailwindCSS initialized\n"
            "- File structure ready: pages/, components/, hooks/\n"
            "- Routing and Redux configured\n"
            "- Output path: `/frontend/`",
            0.95,
        )
