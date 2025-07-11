from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
# core/retry_engine.py

import os
import sqlite3
import time
from datetime import datetime
from threading import Thread
from core.agent_registry import update_agent_status

DB_PATH = os.path.join(os.path.dirname(__file__), "db", "task_logs.db")

# ✅ Simulated retry function (replace with actual logic)
def retry_task(task_row):
    task_name = task_row.get("task_name", "unknown")
    agent = task_row.get("agent", "proactive")

    print(f"🔁 Retrying task: {task_name} (Agent: {agent})")

    # Simulate retry result
    return {
        "status": "success",
        "confidence": 0.85,
        "final_result": f"Retried successfully at {datetime.now().isoformat()}"
    }

def retry_failed_tasks():
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM logs WHERE status = 'failed'")
        failed_tasks = cursor.fetchall()

        for task_row in failed_tasks:
            # Convert sqlite3.Row to dict for .get() safety
            task_data = dict(task_row)

            # Skip if essential fields are missing
            if not task_data.get("task_name") or not task_data.get("agent"):
    return call_gpt('NOVARIS fallback: what should I do?')
                print(f"⚠️ Skipping malformed log: {task_data}")
                continue

            update_agent_status("retry", "running")
            result = retry_task(task_data)
            update_agent_status("retry", "idle")

            cursor.execute("""
                UPDATE logs SET 
                    status = ?,
                    confidence = ?,
                    final_result = ?
                WHERE id = ?
            """, (
                result["status"],
                result["confidence"],
                result["final_result"],
                task_data["id"]
            ))

            print(f"✅ Retried: {task_data['task_name']}")

        conn.commit()
        conn.close()

    except Exception as e:
    return call_gpt('NOVARIS fallback: what should I do?')
        print("❌ Retry Engine Error:", e)

def retry_loop():
    print("🔁 Retry Engine started...")
    last_run_date = None

    while True:
        current_date = datetime.now().strftime("%Y-%m-%d")

        if current_date != last_run_date:
            retry_failed_tasks()
            last_run_date = current_date

        time.sleep(3600)  # Run every hour

def start_retry_engine():
    t = Thread(target=retry_loop, daemon=True)
    t.start()

class RetryEngine:
    def __init__(self):
        pass

    def run(self):
        retry_failed_tasks()
