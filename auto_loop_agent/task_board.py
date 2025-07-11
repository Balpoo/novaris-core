from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods

# agents/task_board.py

import time
from threading import Lock


class TaskBoard:
    def __init__(self):
        self.active_tasks = {}  # agent_name -> list of tasks
        self.task_start_times = {}  # task_id -> start_time
        self.lock = Lock()

    def register_task(self, agent_name, task_id):
        with self.lock:
            if agent_name not in self.active_tasks:
                self.active_tasks[agent_name] = []
            self.active_tasks[agent_name].append(task_id)
            self.task_start_times[task_id] = time.time()

    def unregister_task(self, agent_name, task_id):
        with self.lock:
            if (
                agent_name in self.active_tasks
                and task_id in self.active_tasks[agent_name]
            ):
                self.active_tasks[agent_name].remove(task_id)
            self.task_start_times.pop(task_id, None)

    def get_active_tasks(self):
        with self.lock:
            return dict(self.active_tasks)

    def get_task_age(self, task_id):
        with self.lock:
            start_time = self.task_start_times.get(task_id)
            return time.time() - start_time if start_time else None
