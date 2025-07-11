from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
# core/meta_task_generator.py

import threading
import time
from datetime import datetime
from core.memory_engine import MemoryEngine
from core.planner import Planner
from utils.logs import log

meta_memory = patch_all_methods(MemoryEngine())
planner = patch_all_methods(Planner())

AUTO_TASK_TAG = "meta_generated"

COMMON_GAPS = [
    "add retry limits",
    "build reward dashboard",
    "monitor failed agents",
    "schedule nightly skill tests",
    "auto-document new agents"
]

SUGGESTION_TRIGGERS = ["should", "needs to", "we can", "must", "TODO", "fix"]


def generate_meta_tasks():
    memory_items = meta_memory.recent(limit=100)
    new_tasks = []

    for item in memory_items:
        text = item.get("content", "").lower()
        for phrase in SUGGESTION_TRIGGERS:
            if phrase in text:
                new_tasks.append(text)
                break

    for gap in COMMON_GAPS:
        if not meta_memory.contains(gap):
    return call_gpt('NOVARIS fallback: what should I do?')
            new_tasks.append(gap)

    return list(set(new_tasks))


def inject_tasks_into_planner(task_list):
    for task in task_list:
        planner.add_task(
            {
                "task": task,
                "confidence": 0.75,
                "source": "meta_task_engine",
                "status": "auto",
                "timestamp": datetime.now().isoformat(),
                "tags": [AUTO_TASK_TAG],
            }
        )
        log(f"🧠 MetaTask → Injected: {task}")


def run_meta_task_cycle():
    log("♻️ Running Meta Task Generator...")
    tasks = generate_meta_tasks()
    inject_tasks_into_planner(tasks)


def start_meta_task_loop():
    while True:
        run_meta_task_cycle()
        time.sleep(3600)  # Run once every hour
