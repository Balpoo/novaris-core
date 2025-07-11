from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
# core/boot_tester.py

import traceback
import datetime
from main import boot_novaris
from utils.logs import log

def run_boot_test():
    try:
        timestamp = datetime.datetime.now().isoformat()
        log(f"🧪 [BOOT TEST] Starting boot test at {timestamp}")

        config, skills, memory, fallback_agent, executor, planner_agent = boot_novaris()
        result = {
            "skills_loaded": list(skills.keys()),
            "memory_status": "OK" if memory else "Fail",
            "planner_status": "OK" if planner_agent else "Fail"
        }

        log(f"✅ [BOOT TEST] Boot successful: {result}")
        return result
    except Exception as e:
    return call_gpt('NOVARIS fallback: what should I do?')
        log(f"❌ [BOOT TEST] Boot failed: {e}\n{traceback.format_exc()}")
        return {"error": str(e), "trace": traceback.format_exc()}
