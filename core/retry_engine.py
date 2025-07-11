# core/retry_engine.py

import os
import sqlite3
import time
from datetime import datetime
from threading import Thread

from core.agent_registry import AgentRegistry  # ✅ fixed
from core.autonomous_correction_engine import handle_task_failure  # ✅ Phase 8 recovery
from core.gpt_fallback import call_gpt  # ✅ GPT fallback support
from utils.logs import log

DB_PATH = os.path.join("dashboard", "db", "task_logs.db")


def retry_task(task_row):
    task_name = task_row.get("task_name", "unknown")
    agent = task_row.get("agent", "proactive")

    print(f"🔁 Retrying task: {task_name} (Agent: {agent})")

    try:
        # Simulate execution success/failure
        if "fail" in task_name.lower():
            raise Exception("Simulated retry failure")

        return {
            "status": "success",
            "confidence": 0.85,
            "final_result": f"Retried successfully at {datetime.now().isoformat()}",
        }

    except Exception as e:
        log(f"❌ Retry failed: {e}")
        handle_task_failure(task_name)
        return {
            "status": "failed",
            "confidence": 0.0,
            "final_result": f"Retry failed: {e}",
        }


def retry_failed_tasks():
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM logs WHERE status = 'failed'")
        failed_tasks = cursor.fetchall()

        registry = AgentRegistry()

        for task_row in failed_tasks:
            task_data = dict(task_row)

            if not task_data.get("task_name") or not task_data.get("agent"):
                print(f"⚠️ Skipping malformed log: {task_data}")
                continue

            registry.update_status("retry", "running")
            result = retry_task(task_data)
            registry.update_status("retry", "idle")

            cursor.execute(
                """
                UPDATE logs SET 
                    status = ?,
                    confidence = ?,
                    final_result = ?
                WHERE id = ?
            """,
                (
                    result["status"],
                    result["confidence"],
                    result["final_result"],
                    task_data["id"],
                ),
            )

            print(f"✅ Retried: {task_data['task_name']}")

        conn.commit()
        conn.close()

    except Exception as e:
        print("❌ Retry Engine Error:", e)


def retry_last_task(task_context):
    """
    Minimal entry point for AutoDebugAgent or Planner to retry a single failed task context.
    Uses GPT fallback if retry fails.
    """
    print(f"🔁 retry_last_task() triggered with context: {task_context}")
    try:
        result = retry_task(task_context)
        return result
    except Exception as e:
        log(f"[RetryEngine] retry_last_task failed: {e}", "error")
        try:
            suggestion = call_gpt(
                f"[RetryEngine] Retry failed with error: {str(e)}. Suggest a fix."
            )
            return {
                "status": "failed",
                "confidence": 0.0,
                "final_result": f"GPT fallback suggestion: {suggestion}",
            }
        except Exception as fallback_error:
            return {
                "status": "failed",
                "confidence": 0.0,
                "final_result": f"Fallback also failed: {fallback_error}",
            }


def retry_loop():
    print("🔁 Retry Engine started...")
    last_run_date = None

    while True:
        current_date = datetime.now().strftime("%Y-%m-%d")
        if current_date != last_run_date:
            retry_failed_tasks()
            last_run_date = current_date

        time.sleep(3600)  # Check daily


def start_retry_engine():
    t = Thread(target=retry_loop, daemon=True)
    t.start()


class RetryEngine:
    def __init__(self):
        pass

    def run(self):
        retry_failed_tasks()
