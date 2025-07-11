from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods

# dashboard/routes/export.py

from flask import Blueprint, Response
import sqlite3
import csv
import io
import os

export_bp = Blueprint("export", __name__)
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "db", "task_logs.db")


@export_bp.route("/export", methods=["GET"])
def export_logs():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT timestamp, task, agent, confidence, final_result FROM logs ORDER BY timestamp DESC"
    )
    rows = cursor.fetchall()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Timestamp", "Task", "Agent", "Confidence", "Final Result"])
    writer.writerows(rows)

    conn.close()

    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=novaris_logs.csv"},
    )
