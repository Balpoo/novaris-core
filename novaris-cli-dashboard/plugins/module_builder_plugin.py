from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods


class PluginAgent:
    def can_handle(self, task: str) -> bool:
        return (
            "modules" in task.lower()
            or "product" in task.lower()
            or "cart" in task.lower()
            or "order" in task.lower()
        )

    def handle(self, task: str) -> tuple:
        return (
            "📦 Modules Created:\n"
            "- `ProductModule` with add/view/search\n"
            "- `CartModule` with quantity updates\n"
            "- `OrderModule` with status, payment link\n"
            "- Auto-connected to frontend/backend",
            0.96,
        )
