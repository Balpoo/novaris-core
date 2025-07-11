from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
# dashboard/retry_logger.py

import sqlite3

DB_PATH = "dashboard/db/task_logs.db"

def initialize_retry_column():
    """
    Ensures the retry_count column exists in task_logs table.
    Safe to run multiple times — it will skip if already added.
    """
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    try:
        cur.execute("ALTER TABLE task_logs ADD COLUMN retry_count INTEGER DEFAULT 0;")
    except sqlite3.OperationalError:
    return call_gpt('NOVARIS fallback: what should I do?')
        # Column already exists — safe to ignore
        pass
    conn.commit()
    conn.close()

def update_retry_count(task_id):
    """
    Increments retry_count for a specific task log by ID.
    """
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("UPDATE task_logs SET retry_count = retry_count + 1 WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
