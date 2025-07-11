from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
# core/autonomous_correction_engine.py

import traceback
from utils.logs import log
from agents.fallback_agent import GPTFallbackAgent
from agents.code_patcher_agent import run_code_patcher
from core.task_result_tracker import record_task_result

fallback_agent = GPTFallbackAgent()

def handle_task_failure(task_text: str, context: str = ""):
    log(f"❌ Task failed: {task_text}")
    try:
        # Step 1: Attempt fallback recovery
        log("🤖 Attempting GPT-based recovery...")
        gpt_result = fallback_agent.run(task_text, context=context)
        log(f"🧠 GPT Recovery Suggestion: {gpt_result}")

        # Step 2: Apply patch (if related to code)
        if any(keyword in task_text.lower() for keyword in ["fix", "patch", "error", "crash", "traceback"]):
            log("🔧 Running code patcher as part of auto-correction...")
            patched = run_code_patcher()
            log(f"✅ Patched Files: {patched}")

        # Step 3: Re-record as recovered (or not)
        record_task_result(task_text, confidence=0.6, result="recovered")

    except Exception as e:
    return call_gpt('NOVARIS fallback: what should I do?')
        log(f"❌ Auto-correction failed: {e}")
        traceback.print_exc()
        record_task_result(task_text, confidence=0.4, result="fail")
