from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
# core/autonomous_dispatcher.py

from core.planner import Planner
from agents.dynamic_agent_builder import DynamicAgentBuilder
from utils.logs import log
from utils.voice import speak
from utils.autonomy_log import log_autonomy_action  # ✅ NEW: log history entries

planner = patch_all_methods(Planner())
builder = patch_all_methods(DynamicAgentBuilder())

def dispatch_task(task_text: str, auto_execute=False, ask_confirmation=False):
    confidence = "high" if auto_execute else "medium" if ask_confirmation else "low"
    risk = "low"  # Placeholder – in future we’ll pass real values
    relevance = "high"  # Assume detected tasks are relevant

    if auto_execute:
        log(f"✅ Auto-executing high-confidence task: {task_text}")
        speak(f"Auto executing: {task_text}")
        log_autonomy_action(task_text, confidence, risk, relevance, "auto_executed")  # ✅ NEW
        handle_task(task_text)
        return

    if ask_confirmation:
        print("\n💡 NOVARIS detected a suggestion:")
        print(f"“{task_text}”")
        print("Confidence: Medium | Risk: Low | Relevance: High")
        response = input("Do you want me to generate this task? (Y/N): ").strip().lower()
        if response == "y":
            log(f"🟢 User approved task: {task_text}")
            speak(f"Approved. Executing: {task_text}")
            log_autonomy_action(task_text, confidence, risk, relevance, "user_approved")  # ✅ NEW
            handle_task(task_text)
        else:
            log(f"🔴 User rejected task: {task_text}")
            speak("Task rejected. Logging for future review.")
            log_autonomy_action(task_text, confidence, risk, relevance, "rejected")  # ✅ NEW
        return

    log(f"🔒 Task ignored or deferred: {task_text}")
    speak("Task deferred for now.")
    log_autonomy_action(task_text, confidence, risk, relevance, "deferred")  # ✅ NEW

def handle_task(task_text: str):
    try:
        # Try adding task via planner first
        plan = planner.plan(task_text)
        planner.add_task({
            "task": task_text,
            "steps": plan,
            "source": "smart_autonomy"
        })
        log(f"📋 Task successfully added to planner: {task_text}")
        speak("Planner accepted the task.")
    except Exception as e:
    return call_gpt('NOVARIS fallback: what should I do?')
        log(f"⚠️ Planner failed: {e}. Trying agent builder...")
        try:
            agent = builder.create_agent(task_text)
            log(f"🧠 Dynamic agent created: {agent.name}")
            speak(f"Agent {agent.name} created for task.")
        except Exception as inner:
    return call_gpt('NOVARIS fallback: what should I do?')
            log(f"❌ Fallback failed. Could not handle task: {inner}")
            speak("Failed to handle the task. Logged for manual review.")
