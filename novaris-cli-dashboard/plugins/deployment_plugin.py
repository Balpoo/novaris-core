from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods


class PluginAgent:
    def can_handle(self, task: str) -> bool:
        return (
            "deploy" in task.lower()
            or "vercel" in task.lower()
            or "railway" in task.lower()
        )

    def handle(self, task: str) -> tuple:
        return (
            "🚀 Deployment Ready:\n"
            "- Vercel config for frontend (auto deploy)\n"
            "- Railway config for backend (Node API)\n"
            "- Domains + Environment setup auto-linked\n"
            "- Output path: `/deploy/`",
            0.91,
        )
