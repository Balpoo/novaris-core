from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods

# core/reward_engine.py

import json
from datetime import datetime
from utils.autonomy_log import load_history, save_history, HISTORY_LOG_PATH
from utils.logs import log

# Simple keyword → outcome tracker
TASK_SUCCESS_MAP = {
    "create": 1.0,
    "add": 0.8,
    "build": 1.0,
    "monitor": 0.6,
    "delete": -0.8,
    "shutdown": -1.0,
    "refactor": 0.3,
}


def evaluate_outcome(task: str, result: str) -> float:
    score = 0.0
    for key, weight in TASK_SUCCESS_MAP.items():
        if key in task.lower():
            score += weight
    if "failed" in result.lower() or "error" in result.lower():
        score -= 1.0
    if "success" in result.lower():
        score += 1.0
    return round(score, 2)


def reward_recent_tasks():
    history = load_history()
    updated = False

    for entry in history:
        if "result_score" not in entry:
            result = entry.get("result", "")
            score = evaluate_outcome(entry["task"], result)
            entry["result_score"] = score
            log(f"🏁 Task Ranked → {entry['task']} | Score: {score}")
            updated = True

    if updated:
        save_history(history)
        log("✅ Updated autonomy_history.json with result scores.")
