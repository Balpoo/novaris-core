from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods

# plugins/example_plugin.py


class PluginAgent:
    def can_handle(self, task: str) -> bool:
        return "translate" in task.lower()

    def handle(self, task: str) -> tuple:
        return "Translated to Marathi: 'नमस्कार'", 0.93


# Optional direct-access shortcut for CommandTab plugin trigger
def handle_translation(task: str) -> str:
    return "Translated to Marathi: 'नमस्कार' [via plugin shortcut]"
