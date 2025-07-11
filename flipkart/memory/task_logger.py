from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
import json
import os
from datetime import datetime

MEMORY_FILE = "memory/task_log.jsonl"


def log_task(task, agent, confidence, result):
    os.makedirs(os.path.dirname(MEMORY_FILE), exist_ok=True)
    log = {
        "timestamp": datetime.utcnow().isoformat(),
        "task": task,
        "agent": agent,
        "confidence": confidence,
        "result": result,
    }
    with open(MEMORY_FILE, "a") as f:
        f.write(json.dumps(log) + "\n")
