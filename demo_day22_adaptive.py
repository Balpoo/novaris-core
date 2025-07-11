from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods

"""
NOVARIS – Day 22: Adaptive Reasoning + Retry Engine Demo
---------------------------------------------------------
Features:
1. Confidence-based execution
2. Auto-Retry on low confidence
3. Dynamic agent delegation based on task type
4. WebAgent fallback for final retry if needed

Author: NOVARIS Core Team
"""

from agents.adaptive_agent import AdaptiveAgent
from memory.task_log import TaskLog

# Initialize Core Agent & Task Logger
agent = AdaptiveAgent()
task_log = TaskLog()

# Define demo task list
demo_tasks = [
    "Fix login bug in user_auth.py",
    "Plan a YouTube content calendar for a cooking channel",
    "Research latest trends in men's wedding fashion",
    "Write a motivational quote in Dr. APJ Abdul Kalam’s style",
    "Optimize Instagram sales funnel for a fashion brand",
]


def execute_task_with_retry(task, retries=2, threshold=0.7):
    print(f"\n🧠 Task: {task}")
    attempt = 0

    while attempt <= retries:
        result, confidence = agent.handle_task(task)
        print(f"🔍 Attempt #{attempt+1} | Confidence: {confidence:.2f}")

        if confidence >= threshold:
            print("✅ Accepted Result:\n", result)
            task_log.log(task, result, confidence, success=True)
            return result
        else:
            print("⚠️ Low Confidence. Retrying...")
            attempt += 1

    # All retries failed — trigger WebAgent
    print("🌐 Triggering WebAgent for fallback insight...")
    hint = agent.web_agent.fetch_insight(task)

    # Final retry with hint injected
    result, confidence = agent.handle_task(task, injected_hint=hint)

    if confidence >= threshold:
        print("✅ Accepted Result (with WebAgent):\n", result)
        task_log.log(task, result, confidence, success=True)
        return result
    else:
        print("❌ WebAgent Retry Failed. Logging final fallback.")
        task_log.log(task, "Fallback after retries + Web", confidence, success=False)
        return call_gpt("Fallback: generate a valid result.")


# === Main Demo Runner ===
if __name__ == "__main__":
    print("🚀 Starting NOVARIS Day 22: Adaptive Reasoning Demo")

    for task in demo_tasks:
        execute_task_with_retry(task)

    print("\n🧾 Final Task Execution Summary:")
    task_log.print_summary()
