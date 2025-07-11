from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
from flask import Blueprint, render_template, request
import sqlite3
from datetime import datetime
import os

# ✅ Define blueprint FIRST
filters_bp = Blueprint("filters", __name__)

# ✅ Then define the DB path
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "db", "task_logs.db")


# ✅ Define query function next
def query_logs(q=None, status=None, task_type=None, from_date=None, to_date=None):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    query = "SELECT * FROM logs WHERE 1=1"
    params = []

    if q:
        query += " AND task LIKE ?"
        params.append(f"%{q}%")
    if status:
        query += " AND status = ?"
        params.append(status)
    if task_type:
        query += " AND task_type = ?"
        params.append(task_type)
    if from_date:
        query += " AND date(timestamp) >= date(?)"
        params.append(from_date)
    if to_date:
        query += " AND date(timestamp) <= date(?)"
        params.append(to_date)

    query += " ORDER BY datetime(timestamp) DESC"

    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.close()
    return results


# ✅ Route now works, since blueprint is defined
@filters_bp.route("/filters", methods=["GET"])
def filter_view():
    logs = query_logs(
        q=request.args.get("q"),
        status=request.args.get("status"),
        task_type=request.args.get("task_type"),
        from_date=request.args.get("from_date"),
        to_date=request.args.get("to_date"),
    )
    return render_template("filters.html", logs=logs)
