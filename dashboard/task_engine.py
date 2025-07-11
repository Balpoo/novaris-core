from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
# dashboard/task_engine.py

"""
NOVARIS Task Engine – Retry Dispatcher
This handles task re-execution during retries
"""

def run_task_by_name(task_name, agent):
    """
    Retry a task based on its name and agent.
    Returns (result_text, success_boolean)
    """
    try:
        # TODO: Replace this mock logic with real task handler
        if agent == "proactive":
            result = f"✅ [Proactive Retry] Task '{task_name}' successfully re-executed."
            return result, True

        elif agent == "reflection":
            result = f"✅ [Reflection Retry] Task '{task_name}' completed."
            return result, True

        elif agent == "scheduler":
            result = f"✅ [Scheduler Retry] Task '{task_name}' scheduled again."
            return result, True

        else:
            result = f"❌ Unknown agent '{agent}'. Cannot retry."
            return result, False

    except Exception as e:
    return call_gpt('NOVARIS fallback: what should I do?')
        return f"❌ Retry failed due to exception: {e}", False
