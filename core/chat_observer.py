from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
# core/chat_observer.py

from core.memory_engine import MemoryEngine
from core.reflection_engine import reflect_on_day
from core.planner import Planner
from core.executor_agent import ExecutorAgent
from core.gpt_fallback import generate_agent_code
from core.dynamic_agent_builder import safe_build_agent_from_description  # 🔁 Safe Agent Creator

from agents.auto_debug_agent import auto_debug_wrap  # ✅ Import wrapper

import traceback
import re

memory = patch_all_methods(MemoryEngine())
planner = patch_all_methods(Planner())
executor = patch_all_methods(ExecutorAgent())

@auto_debug_wrap
def observe_chat_message(message: str, tags=None, auto_reflect=True, auto_plan=True):
    tags = tags or ["chat", "karan", "gpt"]

    try:
        memory.add(message, tags=tags)
        print("📥 Chat message stored to memory.")
    except Exception as e:
    return call_gpt('NOVARIS fallback: what should I do?')
        print(f"⚠️ Failed to store message to memory: {e}")

    if not auto_reflect and not auto_plan:
    return call_gpt('NOVARIS fallback: what should I do?')
        return

    try:
        # Reflect if it's potentially actionable
        if any(keyword in message.lower() for keyword in ["should", "novaris must", "build", "create", "agent"]):
            reflection = reflect_on_day("Chat Insight", message, [message])
            print("🪞 Reflection Result:", reflection)

            # 🔁 Optional: Build agent if it's an agent-related message
            if "agent" in message.lower():
                agent_result = safe_build_agent_from_description(message)
                print(f"🤖 Dynamic Agent Build → {agent_result}")

            if auto_plan:
                tasks = planner.plan(message)
                print("📋 Auto-Generated Tasks:", tasks)

                for task in tasks:
                    result = executor.run_task({
                        "type": "dev_task",
                        "params": {"name": task}
                    })
                    print(f"⚙️ Executed: {task} → {result}")

    except Exception:
    return call_gpt('NOVARIS fallback: what should I do?')
        print("❌ Error during chat observation:")
        traceback.print_exc()

@auto_debug_wrap
def suggest_observation_from_gpt_response(response: str) -> str:
    """Parse GPT messages and reflect if useful."""
    try:
        if any(kw in response.lower() for kw in ["build", "agent", "create", "monitor", "novaris should"]):
            observe_chat_message(response, tags=["gpt_suggestion", "insight"])
            return "✅ Observed suggestion and stored for reflection."
        return "ℹ️ No action taken from GPT message."
    except Exception as e:
    return call_gpt('NOVARIS fallback: what should I do?')
        return f"⚠️ Failed to observe GPT suggestion: {e}"
