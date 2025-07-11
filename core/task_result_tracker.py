from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods

# core/task_result_tracker.py

from utils.logs import log


def record_task_result(task: dict, outcome: str):
    # You can enhance this later with DB/file writes
    log(f"[TaskResult] {task.get('task', 'Unknown Task')} → {outcome}")
