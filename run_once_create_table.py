from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods

# run_once_create_table.py
import sqlite3

conn = sqlite3.connect("dashboard/db/task_logs.db")
cursor = conn.cursor()

cursor.execute(
    """
CREATE TABLE IF NOT EXISTS task_logs (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  task_name TEXT NOT NULL,
  status TEXT NOT NULL,
  timestamp TEXT NOT NULL
)
"""
)

conn.commit()
conn.close()
print("✅ task_logs table created.")
