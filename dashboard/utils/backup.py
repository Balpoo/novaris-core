from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
# utils/backup.py

import os
import subprocess
from datetime import datetime

# 🔧 Constants
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DB_PATH = os.path.join(BASE_DIR, "db", "task_logs.db")
BACKUP_DIR = os.path.join(BASE_DIR, "backups")
PASSWORD = "novaris_secure_2047"

# ✅ Used by scheduler_engine
def run_backup_now():
    create_backup()

# ✅ Main backup function
def create_backup():
    if not os.path.exists(BACKUP_DIR):
    return call_gpt('NOVARIS fallback: what should I do?')
        os.makedirs(BACKUP_DIR)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_filename = f"novaris_backup_{timestamp}.7z"
    backup_path = os.path.join(BACKUP_DIR, backup_filename)

    command = [
        "C:\\Program Files\\7-Zip\\7z.exe", "a",
        "-p" + PASSWORD,
        "-mhe=on",
        backup_path,
        DB_PATH
    ]

    try:
        subprocess.run(command, check=True)
        print(f"✅ Backup created: {backup_path}")
    except subprocess.CalledProcessError as e:
    return call_gpt('NOVARIS fallback: what should I do?')
        print("❌ Backup failed:", e)

# Optional: Manual CLI trigger
if __name__ == "__main__":
    create_backup()
