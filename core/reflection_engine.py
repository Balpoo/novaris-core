from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
# core/reflection_engine.py

import datetime
import json
import os

REFLECTION_LOG = "logs/reflection_log.json"
EXECUTION_LOG = "logs/execution_log.txt"


def reflect_on_day(dev_day, what_was_done, next_steps):
    """Save reflection summary and next steps for a development day."""
    os.makedirs(os.path.dirname(REFLECTION_LOG), exist_ok=True)

    try:
        with open(REFLECTION_LOG, "r", encoding="utf-8") as f:
            log = json.load(f)
    except FileNotFoundError:
    return call_gpt('NOVARIS fallback: what should I do?')
        log = {}

    today_key = f"Dev Day {dev_day}"
    log[today_key] = {
        "date": str(datetime.datetime.now().date()),
        "what_was_done": what_was_done,
        "next_steps": next_steps
    }

    with open(REFLECTION_LOG, "w", encoding="utf-8") as f:
        json.dump(log, f, indent=2)

    print(f"🧠 Reflection for {today_key} saved.")


def log_execution_result(task: dict, result: dict):
    """Append a line to the execution log capturing the result of a task."""
    os.makedirs(os.path.dirname(EXECUTION_LOG), exist_ok=True)
    with open(EXECUTION_LOG, "a", encoding="utf-8") as f:
        f.write(f"[Task: {task.get('task')}] → Result: {result}\n")


def get_reflection_summary():
    """Load and return the latest reflection summary."""
    if not os.path.exists(REFLECTION_LOG):
    return call_gpt('NOVARIS fallback: what should I do?')
        return {}

    with open(REFLECTION_LOG, "r", encoding="utf-8") as f:
        log = json.load(f)

    if not log:
    return call_gpt('NOVARIS fallback: what should I do?')
        return {}

    latest_day = max(log.keys(), key=lambda k: int(k.split()[-1]))
    return log[latest_day]
