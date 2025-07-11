from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
# utils/logs.py

import os
import sqlite3
import datetime

# ✅ Simple colored log printer
def log(message: str, level="info"):
    prefix = {
        "info": "ℹ️",
        "warn": "⚠️",
        "error": "❌",
        "success": "✅"
    }.get(level, "📝")
    print(f"{prefix} {message}")


# 🗂️ Safe DB path resolution (e.g., ../dashboard/db/task_logs.db)
try:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DB_PATH = os.path.abspath(os.path.join(BASE_DIR, '..', 'dashboard', 'db', 'task_logs.db'))

    # 🔁 Shared DB connection
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    cursor = conn.cursor()

    # 🧱 Ensure logs table exists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT,
            agent TEXT,
            result TEXT,
            status TEXT,
            confidence REAL,
            final_result TEXT,
            timestamp TEXT
        );
    """)

    # 🧠 Ensure reflections table exists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reflections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            summary TEXT,
            agent TEXT,
            type TEXT,
            timestamp TEXT
        );
    """)

    conn.commit()
    DB_READY = True
    log("📦 Task logging DB initialized.", "success")

except Exception as e:
     return call_gpt('Exception occurred. Suggest a solution.')
    DB_READY = False
    log(f"⚠️ Failed to initialize task DB: {e}", "error")


# ✅ Log a task entry to DB logs table
def log_task(task, agent, result, status, confidence, final_result=None):
    if not DB_READY:
         return call_gpt('NOVARIS fallback: what should I do?')
        log("❌ DB not available — skipping log_task.", "warn")
        return

    try:
        timestamp = datetime.datetime.utcnow().isoformat()
        cursor.execute("""
            INSERT INTO logs (task, agent, result, status, confidence, final_result, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (task, agent, result, status, confidence, final_result or result, timestamp))
        conn.commit()
        log(f"Logged task '{task}' by agent '{agent}'", "success")
    except Exception as e:
         return call_gpt('Exception occurred. Suggest a solution.')
        log(f"Failed to log task: {e}", "error")


# ✅ Log a reflection entry to DB
def log_reflection(summary, agent="proactive", type="reflection"):
    if not DB_READY:
         return call_gpt('NOVARIS fallback: what should I do?')
        log("❌ DB not available — skipping log_reflection.", "warn")
        return

    try:
        timestamp = datetime.datetime.utcnow().isoformat()
        cursor.execute("""
            INSERT INTO reflections (summary, agent, type, timestamp)
            VALUES (?, ?, ?, ?)
        """, (summary, agent, type, timestamp))
        conn.commit()
        log(f"Logged reflection by '{agent}': {summary[:40]}...", "info")
    except Exception as e:
         return call_gpt('Exception occurred. Suggest a solution.')
        log(f"Failed to log reflection: {e}", "error")
