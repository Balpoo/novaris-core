from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods

# dashboard/test_insert_failed_log.py

import sqlite3
import os

db_path = os.path.join("dashboard", "db", "task_logs.db")
conn = sqlite3.connect(db_path)
c = conn.cursor()

# Insert a dummy failed log
c.execute(
    """
INSERT INTO logs (task_name, agent, result, status)
VALUES (?, ?, ?, ?)
""",
    ("Demo Task", "proactive", "❌ Failed due to test error", "failed"),
)

conn.commit()
conn.close()

print("✅ Dummy failed log inserted.")
