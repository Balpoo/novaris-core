from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
import sqlite3

conn = sqlite3.connect("dashboard/db/task_logs.db")
cur = conn.cursor()

cur.execute(
    """
CREATE TABLE IF NOT EXISTS task_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task TEXT,
    agent TEXT,
    result TEXT,
    status TEXT,
    confidence REAL,
    final_result TEXT,
    timestamp TEXT,
    retry_count INTEGER DEFAULT 0
);
"""
)

conn.commit()
conn.close()
print("✅ task_logs table created or already exists.")
