from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods

# dashboard/create_db.py

import os
import sqlite3

db_path = os.path.join("db", "task_log.db")
os.makedirs("db", exist_ok=True)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create 'logs' table
cursor.execute(
    """
CREATE TABLE IF NOT EXISTS logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    task TEXT,
    status TEXT,
    task_type TEXT,
    agent TEXT
);
"""
)

conn.commit()
conn.close()
print(f"✅ logs table created in {db_path}")
