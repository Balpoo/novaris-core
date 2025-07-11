# agents/auto_debug_agent.py

import traceback
import sys
import os
import re

from core.self_heal_engine import run_self_diagnosis
from core.retry_engine import retry_last_task
from utils.logs import log

DEBUG_LOG = "logs/auto_debug_log.json"
os.makedirs("logs", exist_ok=True)


def log_debug_event(error_type, detail):
    try:
        with open(DEBUG_LOG, "a", encoding="utf-8") as f:
            f.write(f"{error_type} | {detail}\n")
    except Exception as e:
        log(f"⚠️ Failed to write to debug log: {e}", level="error")


def try_auto_patch_from_trace(tb_str):
    try:
        missing_method_match = re.search(
            r"'(.+)' object has no attribute '(.+)'", tb_str
        )
        missing_module_match = re.search(r"No module named '(.+)'", tb_str)

        if missing_method_match:
            cls_name, method = missing_method_match.groups()
            log(f"🔧 Missing method: {method} in class {cls_name}")
            log_debug_event("MissingMethod", f"{cls_name}.{method}")
            run_self_diagnosis()
            return True

        elif missing_module_match:
            module = missing_module_match.group(1)
            log(f"📦 Missing module: {module}, attempting pip install...")
            log_debug_event("MissingModule", module)
            os.system(f"pip install {module}")
            return True

    except Exception as e:
        log(f"⚠️ Failed during auto-patch detection: {e}")

    return False


def auto_debug_wrap(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            tb_str = traceback.format_exc()
            log("❌ Runtime Error Caught. Triggering AutoDebugAgent...", level="error")
            log(tb_str)
            log_debug_event("Exception", str(e))

            try:
                if try_auto_patch_from_trace(tb_str):
                    log("♻️ Retrying after auto-patch...")
                    retry_last_task()
                else:
                    log(
                        "🛑 Auto-patch not possible. Manual intervention needed.",
                        level="error",
                    )
                    raise e
            except Exception as inner_e:
                log(f"⚠️ Auto-debug retry failed: {inner_e}", level="error")
                raise inner_e

    return wrapper


# ✅ Fallback class to support manual GPT-based debug agent
class AutoDebugAgent:
    def __init__(self):
        self.name = "AutoDebugAgent"

    def can_handle(self, task: str) -> bool:
        return "debug" in task.lower() or "error" in task.lower()

    def handle(self, task_context: dict):
        log(f"[{self.name}] Handling task: {task_context}")
        try:
            result = retry_last_task(task_context)
            log(f"[{self.name}] Retry result: {result}")
            return result
        except Exception as e:
            log(f"❌ AutoDebugAgent failed during retry: {e}", level="error")
            return f"⚠️ Failed to auto-debug: {e}"
