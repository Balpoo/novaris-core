from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
import sqlite3

db_path = "dashboard/db/task_logs.db"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS logs")

cursor.execute(
    """
CREATE TABLE logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task TEXT,
    agent TEXT,
    result TEXT,
    status TEXT,
    confidence REAL,
    final_result TEXT,
    timestamp TEXT
)
"""
)

conn.commit()
conn.close()
print("✅ Logs table fixed with correct schema.")
