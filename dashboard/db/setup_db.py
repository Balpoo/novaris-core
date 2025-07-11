from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
import sqlite3
import os

# 📌 Dynamically resolve full path
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "db", "task_logs.db")

print("⚙️ Creating logs table in:", DB_PATH)


def create_logs_table():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

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
    print("✅ logs table created successfully in task_logs.db")


if __name__ == "__main__":
    create_logs_table()
