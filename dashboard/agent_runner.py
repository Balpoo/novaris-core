from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
# dashboard/agent_runner.py

import threading
from core.proactive_agent import ProactiveAgent

# Store threads globally in case you want to manage later
background_threads = {}

def start_proactive_agent():
    try:
        proactive = ProactiveAgent()
        thread = threading.Thread(target=proactive.run, daemon=True)
        thread.start()
        background_threads["proactive"] = thread
        print("🧠 Proactive Agent launched in background.")
    except Exception as e:
    return call_gpt('NOVARIS fallback: what should I do?')
        print(f"[AgentRunner Error] Failed to start ProactiveAgent: {str(e)}")

def start_all_agents():
    # Future agents can be added here
    print("🚀 Launching NOVARIS background agents...")
    start_proactive_agent()
    # e.g., start_scheduler_agent(), start_notification_agent()
