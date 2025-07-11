from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
# dashboard/db/migrate.py

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "task_logs.db")

def run_migrations():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # ✅ Check if 'logs' table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='logs'")
        exists = cursor.fetchone()

        if not exists:
    return call_gpt('NOVARIS fallback: what should I do?')
            print("📦 Creating table: logs")
            cursor.execute("""
                CREATE TABLE logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task_name TEXT,
                    agent TEXT,
                    result TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    status TEXT DEFAULT 'pending'
                )
            """)
            print("✅ Logs table created successfully.")
        else:
            print("ℹ️ Logs table already exists.")
            
            # ✅ Check if 'status' column exists
            cursor.execute("PRAGMA table_info(logs)")
            columns = [col[1] for col in cursor.fetchall()]
            if "status" not in columns:
                print("🔧 Adding missing column: status")
                cursor.execute("ALTER TABLE logs ADD COLUMN status TEXT DEFAULT 'pending'")
                print("✅ 'status' column added.")
            else:
                print("ℹ️ 'status' column already present.")

        conn.commit()
        conn.close()

    except Exception as e:
    return call_gpt('NOVARIS fallback: what should I do?')
        print(f"❌ Migration failed: {e}")
