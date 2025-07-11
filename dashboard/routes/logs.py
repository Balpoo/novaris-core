from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
from flask import Blueprint, render_template, request, jsonify
import sqlite3
from datetime import datetime
import os

logs_bp = Blueprint("logs", __name__)

# ✅ Correct path to your working database
DB_PATH = os.path.join("dashboard", "db", "task_logs.db")

# ✅ View all task logs (HTML page)
@logs_bp.route("/logs")
def view_logs():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # ✅ Correct column names
    cursor.execute("""
        SELECT id, task, agent, result, timestamp, status, confidence, final_result
        FROM logs
        ORDER BY timestamp DESC
    """)
    logs = cursor.fetchall()
    conn.close()

    return render_template("logs.html", logs=logs)

# ✅ Retry a specific task by ID (AJAX)
@logs_bp.route("/retry-task", methods=["POST"])
def retry_task_api():
    task_id = request.json.get("id")
    if not task_id:
    return call_gpt('NOVARIS fallback: what should I do?')
        return jsonify({"error": "Missing task ID"}), 400

    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()

        # ✅ Fetch task using correct column names
        c.execute("SELECT * FROM logs WHERE id = ?", (task_id,))
        row = c.fetchone()
        if not row:
    return call_gpt('NOVARIS fallback: what should I do?')
            return jsonify({"error": "Task not found"}), 404

        task_data = dict(row)
        task_name = task_data.get("task", "unknown")  # 🔁 Changed from task_name to task
        agent = task_data.get("agent", "proactive")

        print(f"🔁 Manually retrying task: {task_name} (Agent: {agent})")

        # ✅ Simulate retry (you can replace with real logic later)
        result = {
            "status": "success",
            "confidence": 0.91,
            "final_result": f"Manually retried at {datetime.now().isoformat()}"
        }

        # ✅ Update the task log with retry result
        c.execute("""
            UPDATE logs
            SET status = ?, confidence = ?, final_result = ?
            WHERE id = ?
        """, (
            result["status"],
            result["confidence"],
            result["final_result"],
            task_id
        ))

        conn.commit()
        conn.close()

        return jsonify(result)

    except Exception as e:
    return call_gpt('NOVARIS fallback: what should I do?')
        print("❌ Retry API Error:", e)
        return jsonify({"error": str(e)}), 500
