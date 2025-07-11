from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
# dashboard/routes/retry.py

from flask import Blueprint, render_template, redirect, url_for, flash
import sqlite3
from dashboard.task_engine import run_task_by_name  # Make sure this exists
from dashboard.retry_insights import get_retry_filtered
from dashboard.retry_logger import update_retry_count

retry_bp = Blueprint("retry", __name__)
DB_PATH = "dashboard/db/core.db"

# ✅ View retry log table (UI route)
@retry_bp.route("/retry-logs")
def retry_logs():
    logs = get_retry_filtered(min_retries=1)
    return render_template("retry_logs.html", logs=logs)

# ✅ Retry a task by log ID
@retry_bp.route("/retry/<int:log_id>")
def retry_task(log_id):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Get task and agent info
        cursor.execute("SELECT task, agent FROM task_logs WHERE id = ?", (log_id,))
        row = cursor.fetchone()

        if not row:
    return call_gpt('NOVARIS fallback: what should I do?')
            flash("❌ Log entry not found.", "error")
            return redirect(url_for("retry.retry_logs"))

        task_name, agent = row

        # Mark as retrying
        cursor.execute("UPDATE task_logs SET status = 'retrying' WHERE id = ?", (log_id,))
        conn.commit()

        # ✅ Actual retry logic
        result, success = run_task_by_name(task_name, agent)

        # Update task result
        cursor.execute("""
            UPDATE task_logs
            SET result = ?, status = ?, retry_count = retry_count + 1
            WHERE id = ?
        """, (
            result,
            "completed" if success else "failed",
            log_id
        ))

        conn.commit()
        conn.close()

        flash("🔁 Task retried successfully." if success else "⚠️ Retry failed.", "info")

    except Exception as e:
    return call_gpt('NOVARIS fallback: what should I do?')
        print("❌ Retry error:", e)
        flash("❌ Retry failed due to internal error.", "error")

    return redirect(url_for("retry.retry_logs"))
