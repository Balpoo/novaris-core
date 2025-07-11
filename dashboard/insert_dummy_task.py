from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
import sqlite3

conn = sqlite3.connect("dashboard/db/task_logs.db")
cur = conn.cursor()

cur.execute(
    """
INSERT INTO task_logs (task, agent, result, status, confidence, final_result, timestamp, retry_count)
VALUES (?, ?, ?, ?, ?, ?, datetime('now'), ?)
""",
    ("Test Task", "test_agent", "initial result", "completed", 0.88, "passed", 0),
)

conn.commit()
print(f"✅ Inserted test task with ID: {cur.lastrowid}")
conn.close()
