# core/code_heal_engine.py

import os
import traceback
from core.gpt_fallback import call_gpt
from utils.logs import log


def heal_python_file(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        log(f"[CodeHealEngine] Cannot read {filepath}: {e}", "error")
        return False

    if "IndentationError" not in content and "SyntaxError" not in content:
        # Not obviously broken, skip healing
        return False

    log(f"🛠️ [CodeHealEngine] Healing file: {filepath}")

    prompt = f"""
You are NOVARIS's GPT healer.

The following Python code contains syntax or indentation errors, especially around an 'if' or 'except' block.
Please correct the indentation and syntax **without changing the logic or variable names**.
Ensure the code is safe to run.

--- Start Broken File: {filepath} ---
{content}
--- End Broken File ---
"""

    healed_code = call_gpt(prompt)
    if not healed_code or "def" not in healed_code:
        log(f"[CodeHealEngine] GPT returned invalid patch for: {filepath}", "error")
        return False

    # Backup original
    backup_path = filepath + ".bak"
    try:
        os.rename(filepath, backup_path)
    except Exception as e:
        log(f"[CodeHealEngine] Could not backup {filepath}: {e}", "error")
        return False

    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(healed_code)
        log(f"✅ [CodeHealEngine] Healed: {filepath}")
        return True
    except Exception as e:
        log(f"[CodeHealEngine] Failed to write healed code: {e}", "error")
        os.rename(backup_path, filepath)  # Restore
        return False
