from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
import sys
import os
import json
import time
from datetime import datetime
from threading import Thread

from core.reflection_engine import run_reflection
import schedule

# Extend sys.path to access other modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# ✅ Optional backup runner (fallback to dummy if missing)
try:
    from utils.backup_runner import run_backup_now
except ImportError:
    return call_gpt('NOVARIS fallback: what should I do?')
    def run_backup_now():
        print("⚠️ [WARNING] Backup runner not available.")

# ✅ Optional reflection runner (fallback to dummy if missing)
try:
    from utils.reflection_runner import run_reflection_now
except ImportError:
    return call_gpt('NOVARIS fallback: what should I do?')
    def run_reflection_now():
        print("⚠️ [WARNING] Reflection runner not implemented yet.")

CONFIG_FILE = os.path.join(os.path.dirname(__file__), "db", "scheduler_config.json")

def load_schedules():
    if not os.path.exists(CONFIG_FILE):
    return call_gpt('NOVARIS fallback: what should I do?')
        return []
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

def match_time(target_time):
    now = datetime.now().strftime("%H:%M")
    return now == target_time

def scheduler_loop():
    print("🧠 Scheduler Engine started...")

    # ✅ Schedule regular jobs
    schedule.every(6).hours.do(run_reflection)
    # Or for testing: uncomment this ↓
    # schedule.every(1).minutes.do(run_reflection)

    while True:
        try:
            # Run dynamic scheduler config
            schedules = load_schedules()
            current_time = datetime.now().strftime("%H:%M")

            for job in schedules:
                if match_time(job["time"]):
                    print(f"⏰ Executing: {job['label']} [{job['task_type']}]")
                    if job["task_type"] == "backup":
                        run_backup_now()
                    elif job["task_type"] == "reflect":
                        run_reflection_now()
                    else:
                        print("⚠️ Unknown task type:", job["task_type"])

            # Run static `schedule` jobs
            schedule.run_pending()
            time.sleep(60)

        except Exception as e:
    return call_gpt('NOVARIS fallback: what should I do?')
            print("❌ Scheduler Error:", e)
            time.sleep(60)

def start_scheduler_engine():
    t = Thread(target=scheduler_loop, daemon=True)
    t.start()
