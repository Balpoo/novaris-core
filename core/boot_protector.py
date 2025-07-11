# core/boot_protector.py

import os
import shutil
import traceback
from core.gpt_fallback import gpt_generate_code
from utils.logs import log

BACKUP_ROOT = "backup"
EXCLUDE_DIRS = {"venv", "__pycache__", ".git", "logs"}
TARGET_EXT = ".py"


def validate_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            code = f.read()
        compile(code, path, "exec")
        return True
    except SyntaxError as e:
        log(f"❌ Syntax error in {path}: {e}", level="error")
        return False
    except Exception as e:
        log(f"⚠️ Failed to validate {path}: {e}", level="warn")
        return False


def is_gpt_safe(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return "# GPT-SAFE" in f.read()
    except:
        return False


def backup_file(path):
    backup_path = os.path.join(BACKUP_ROOT, path)
    os.makedirs(os.path.dirname(backup_path), exist_ok=True)
    shutil.copy2(path, backup_path)


def restore_from_backup(path):
    backup_path = os.path.join(BACKUP_ROOT, path)
    if os.path.exists(backup_path):
        shutil.copy2(backup_path, path)
        log(f"🔁 Restored {path} from backup.", level="info")
        return True
    return False


def protect_all_code(root="."):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
        for file in filenames:
            if not file.endswith(TARGET_EXT):
                continue

            rel_path = os.path.relpath(os.path.join(dirpath, file), root)

            # Skip GPT-safe files
            if is_gpt_safe(rel_path):
                log(f"🛡️ Skipped protected file: {rel_path}")
                continue

            try:
                # Backup original if not already backed up
                backup_path = os.path.join(BACKUP_ROOT, rel_path)
                if not os.path.exists(backup_path):
                    backup_file(rel_path)
                    log(f"📦 Backed up: {rel_path}", level="info")

                if not validate_file(rel_path):
                    # Try restoring from backup
                    if restore_from_backup(rel_path) and validate_file(rel_path):
                        continue

                    # If backup also fails, regenerate with GPT
                    log(f"⚠️ Attempting GPT regeneration for: {rel_path}")
                    purpose = f"Rebuild file: {rel_path} with valid logic"
                    try:
                        code = gpt_generate_code(purpose)
                        with open(rel_path, "w", encoding="utf-8") as f:
                            f.write(code)
                        log(f"✅ GPT regenerated file: {rel_path}", level="success")
                    except Exception as e:
                        tb = traceback.format_exc()
                        log(
                            f"❌ GPT regeneration failed for {rel_path}: {e}\n{tb}",
                            level="error",
                        )

            except Exception as e:
                tb = traceback.format_exc()
                log(
                    f"❌ File protection failed for {rel_path}: {e}\n{tb}",
                    level="error",
                )
