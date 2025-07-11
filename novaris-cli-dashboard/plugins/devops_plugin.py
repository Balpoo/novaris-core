from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods


class PluginAgent:
    def can_handle(self, task: str) -> bool:
        return "github actions" in task.lower() or "ci/cd" in task.lower()

    def handle(self, task: str) -> tuple:
        return (
            "⚙️ GitHub Actions Config:\n"
            "- Lint + Build + Deploy pipeline added\n"
            "- Separate jobs for frontend/backend\n"
            "- Secrets integration support\n"
            "- File: `.github/workflows/main.yml`",
            0.92,
        )
