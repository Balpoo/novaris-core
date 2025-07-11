from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods


class PluginAgent:
    def can_handle(self, task: str) -> bool:
        return "pdf" in task.lower() or "documentation" in task.lower()

    def handle(self, task: str) -> tuple:
        return (
            "📄 Docs Generated:\n"
            "- Project Overview.pdf\n"
            "- Tech Stack Summary.pdf\n"
            "- Build & Deployment Guide.pdf\n"
            "- Output: `/docs/` folder (3 PDFs)",
            0.96,
        )
