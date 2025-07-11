from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods

# dashboard/db/fix_nulls.py

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "task_logs.db")


def repair_null_fields():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Replace NULLs with defaults
    cursor.execute("UPDATE logs SET confidence = 0.0 WHERE confidence IS NULL")
    cursor.execute(
        "UPDATE logs SET final_result = 'No result yet.' WHERE final_result IS NULL"
    )
    cursor.execute("UPDATE logs SET task = 'Unnamed Task' WHERE task IS NULL")
    cursor.execute("UPDATE logs SET agent = 'unknown_agent' WHERE agent IS NULL")

    conn.commit()
    conn.close()
    print("✅ Repaired all NULL fields.")


if __name__ == "__main__":
    repair_null_fields()
