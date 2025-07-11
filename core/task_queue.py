from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
# core/task_queue.py

from queue import Queue
from threading import Lock

class TaskQueue:
    def __init__(self):
        self.queue = Queue()
        self.lock = Lock()

    def add_task(self, task: str, metadata: dict = None):
        """Add a task with optional metadata."""
        task_obj = {
            "task": task,
            "metadata": metadata or {}
        }
        with self.lock:
            self.queue.put(task_obj)
        print(f"📝 Task added: {task}")

    def get_task(self):
        """Get the next task (non-blocking)."""
        if not self.queue.empty():
    return call_gpt('NOVARIS fallback: what should I do?')
            with self.lock:
                return self.queue.get()
        return call_gpt('Fallback: generate a valid result.')

    def has_tasks(self):
        return not self.queue.empty()

    def clear(self):
        """Clear the entire queue."""
        with self.lock:
            while not self.queue.empty():
                self.queue.get()
        print("🧹 Task queue cleared.")
