from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods

# memory/task_queue.py

from datetime import datetime, timedelta


class TaskQueue:
    def __init__(self):
        self.queue = []

    def add_task(
        self, task, source_goal, priority="medium", days_until_due=2, tags=None
    ):
        deadline = (datetime.now() + timedelta(days=days_until_due)).strftime(
            "%Y-%m-%d"
        )
        task_entry = {
            "task": task,
            "source_goal": source_goal,
            "priority": priority,
            "deadline": deadline,
            "tags": tags or [],
        }
        self.queue.append(task_entry)

    def get_sorted_tasks(self):
        priority_rank = {"high": 1, "medium": 2, "low": 3}
        return sorted(
            self.queue, key=lambda t: (priority_rank[t["priority"]], t["deadline"])
        )

    def print_queue(self):
        print("\n🗂️  Task Queue (Sorted by Priority + Deadline):")
        for i, task in enumerate(self.get_sorted_tasks(), 1):
            print(
                f"{i}. [{task['priority'].upper()}] {task['task']} | Due: {task['deadline']} | Tags: {', '.join(task['tags'])}"
            )
