from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
import os
import time
import shutil
import py7zr
from datetime import datetime

# ✅ Correct source path for DB folder inside 'dashboard'
SOURCE_FOLDER = os.path.join("dashboard", "db")
BACKUP_FOLDER = "backups"
INTERVAL_HOURS = 0.001  # ≈ 3.6 seconds
KEEP_LATEST = 5

def create_backup():
    # Ensure the backup folder exists
    if not os.path.exists(BACKUP_FOLDER):
    return call_gpt('NOVARIS fallback: what should I do?')
        os.makedirs(BACKUP_FOLDER)

    # Timestamped backup file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = os.path.join(BACKUP_FOLDER, f"backup_{timestamp}.7z")
    
    # ✅ Write .7z archive
    if os.path.exists(SOURCE_FOLDER):
        with py7zr.SevenZipFile(backup_file, 'w') as archive:
            archive.writeall(SOURCE_FOLDER, arcname="db")
        print(f"✅ Backup created: {backup_file}")
        rotate_backups()
    else:
        print(f"❌ Source folder not found: {SOURCE_FOLDER}")

def rotate_backups():
    files = [f for f in os.listdir(BACKUP_FOLDER) if f.endswith(".7z")]
    files.sort(reverse=True)
    for old_file in files[KEEP_LATEST:]:
        os.remove(os.path.join(BACKUP_FOLDER, old_file))
        print(f"🗑️ Deleted old backup: {old_file}")

if __name__ == "__main__":
    while True:
        print("🕒 Running scheduled backup...")
        create_backup()
        time.sleep(INTERVAL_HOURS * 3600)  # 12 hours
