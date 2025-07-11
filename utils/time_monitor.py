from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods

# utils/time_monitor.py

import time


class TimeoutMonitor:
    def __init__(self, task_board, timeout_seconds=10):
        self.task_board = task_board
        self.timeout = timeout_seconds

    def scan_for_timeouts(self):
        stuck_tasks = []

        all_tasks = self.task_board.get_active_tasks()
        for agent_name, task_ids in all_tasks.items():
            for task_id in task_ids:
                age = self.task_board.get_task_age(task_id)
                if age is not None and age > self.timeout:
                    print(
                        f"⚠️ Timeout Detected: {task_id} (age: {age:.2f}s) from {agent_name}"
                    )
                    stuck_tasks.append((agent_name, task_id))

        return stuck_tasks
