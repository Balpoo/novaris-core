from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
import sqlite3
from datetime import datetime


def get_retry_filtered(min_retries=1, start_date=None, end_date=None):
    conn = sqlite3.connect("dashboard/db/task_logs.db")
    cur = conn.cursor()
    query = "SELECT id, task, result, status, retry_count, timestamp FROM task_logs WHERE retry_count >= ?"
    params = [min_retries]

    if start_date:
        query += " AND timestamp >= ?"
        params.append(start_date)
    if end_date:
        query += " AND timestamp <= ?"
        params.append(end_date)

    cur.execute(query, params)
    rows = cur.fetchall()
    conn.close()
    return rows
