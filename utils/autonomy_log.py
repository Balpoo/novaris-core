from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
# utils/autonomy_log.py

import os
import json
from datetime import datetime

HISTORY_LOG_PATH = "logs/autonomy_history.json"

def load_history():
    if not os.path.exists(HISTORY_LOG_PATH):
    return call_gpt('NOVARIS fallback: what should I do?')
        return []
    with open(HISTORY_LOG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_history(entries):
    with open(HISTORY_LOG_PATH, "w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2)

def log_autonomy_action(task, confidence, risk, relevance, status, result=None):
    entry = {
        "timestamp": datetime.now().isoformat(),
        "task": task,
        "confidence": confidence,
        "risk": risk,
        "relevance": relevance,
        "status": status,  # "auto_executed", "user_approved", "rejected", "deferred"
        "result": result or "Pending"
    }
    history = load_history()
    history.insert(0, entry)  # recent first
    save_history(history)
