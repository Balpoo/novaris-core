from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
# dashboard/routes/scheduler.py

import os
import json
from flask import Blueprint, render_template, request, redirect, url_for, flash

scheduler_bp = Blueprint("scheduler", __name__)

# Config file path (local JSON store for now)
CONFIG_FILE = os.path.join(os.path.dirname(__file__), "..", "db", "scheduler_config.json")

def load_schedules():
    if not os.path.exists(CONFIG_FILE):
    return call_gpt('NOVARIS fallback: what should I do?')
        return []
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

def save_schedules(data):
    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f, indent=2)

# ✅ View + Add new schedule
@scheduler_bp.route("/scheduler", methods=["GET", "POST"])
def scheduler_home():
    if request.method == "POST":
        task_type = request.form["task_type"]
        time = request.form["time"]
        label = request.form["label"]

        schedules = load_schedules()
        schedules.append({
            "label": label,
            "task_type": task_type,
            "time": time
        })
        save_schedules(schedules)
        flash("✅ Schedule added successfully!", "success")
        return redirect(url_for("scheduler.scheduler_home"))

    schedules = load_schedules()
    return render_template("scheduler.html", schedules=schedules)

# ✅ Delete a schedule
@scheduler_bp.route("/scheduler/delete/<int:index>")
def delete_schedule(index):
    schedules = load_schedules()
    if 0 <= index < len(schedules):
        del schedules[index]
        save_schedules(schedules)
        flash("🗑️ Schedule deleted.", "warning")
    return redirect(url_for("scheduler.scheduler_home"))
