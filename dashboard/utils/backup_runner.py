from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods

# utils/backup_runner.py


def run_backup_now():
    print("🔁 [BackupRunner] Triggering backup manually...")
    # 🔧 Add actual backup logic or call your backup blueprint if needed
    return "Backup completed"
