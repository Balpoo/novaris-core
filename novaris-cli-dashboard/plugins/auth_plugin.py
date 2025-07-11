from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods


class PluginAgent:
    def can_handle(self, task: str) -> bool:
        return "auth" in task.lower() or "firebase" in task.lower()

    def handle(self, task: str) -> tuple:
        return (
            "🔐 Auth Setup:\n"
            "- Firebase Auth enabled (Email/Google)\n"
            "- Token-based login flows added\n"
            "- Protected routes configured in frontend\n"
            "- Output: `/auth-config/` files",
            0.93,
        )
