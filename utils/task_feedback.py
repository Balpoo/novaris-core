from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods

# utils/task_feedback.py

import time
import sys


def show_task_feedback(task: str, status: str = "Started"):
    sys.stdout.write(f"\r⏳ {task}... {status}")
    sys.stdout.flush()
    time.sleep(0.5)


def complete_task_feedback(result: str):
    sys.stdout.write(f"\r✅ Completed: {result}\n")
