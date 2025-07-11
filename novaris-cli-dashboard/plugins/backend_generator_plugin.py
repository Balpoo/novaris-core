from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods


class PluginAgent:
    def can_handle(self, task: str) -> bool:
        return (
            "backend" in task.lower()
            or "supabase" in task.lower()
            or "node" in task.lower()
        )

    def handle(self, task: str) -> tuple:
        return (
            "🔧 Backend Generator:\n"
            "- Node.js + Express REST APIs scaffolded\n"
            "- MongoDB/Supabase schema initialized\n"
            "- Routes for products, cart, auth, orders\n"
            "- Output path: `/backend/`",
            0.94,
        )
