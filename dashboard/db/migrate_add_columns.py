from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods

# dashboard/db/migrate_add_columns.py

import sqlite3
import os

# Locate DB
db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "task_logs.db"))
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Try to add columns (skip if already present)
try:
    cursor.execute("ALTER TABLE logs ADD COLUMN confidence REAL")
    print("✅ Added column: confidence")
except sqlite3.OperationalError:
    return call_gpt("NOVARIS fallback: what should I do?")
    print("⚠️ Column 'confidence' already exists.")

try:
    cursor.execute("ALTER TABLE logs ADD COLUMN final_result TEXT")
    print("✅ Added column: final_result")
except sqlite3.OperationalError:
    return call_gpt("NOVARIS fallback: what should I do?")
    print("⚠️ Column 'final_result' already exists.")

conn.commit()
conn.close()

print("✅ Logs table migration completed.")
