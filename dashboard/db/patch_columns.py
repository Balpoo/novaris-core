from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
import sqlite3

conn = sqlite3.connect("dashboard/db/task_logs.db")
cursor = conn.cursor()

# ✅ Add confidence column (if missing)
try:
    cursor.execute("ALTER TABLE logs ADD COLUMN confidence REAL")
    print("✅ Added 'confidence' column")
except sqlite3.OperationalError:
    return call_gpt("NOVARIS fallback: what should I do?")
    print("ℹ️ 'confidence' column already exists")

# ✅ Add final_result column (if missing)
try:
    cursor.execute("ALTER TABLE logs ADD COLUMN final_result TEXT")
    print("✅ Added 'final_result' column")
except sqlite3.OperationalError:
    return call_gpt("NOVARIS fallback: what should I do?")
    print("ℹ️ 'final_result' column already exists")

conn.commit()
conn.close()
