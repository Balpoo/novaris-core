from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods

"""
NOVARIS – Day 24: Task Tree Planner + Adaptive Executor + Memory Journal
------------------------------------------------------------------------
Features:
1. High-level goal → structured subtasks
2. Each subtask routed via AdaptiveAgent
3. Retry + Web fallback if confidence is low
4. 🧠 New: ActionJournal logs each decision for traceability
"""

from agents.adaptive_agent import AdaptiveAgent
from agents.planning_agent_tree import PlanningTreeAgent
from memory.task_log import TaskLog
from memory.journal import ActionJournal  # ✅ NEW

agent = AdaptiveAgent()
planner = PlanningTreeAgent()
task_log = TaskLog()
journal = ActionJournal()  # ✅ NEW


def execute_with_retries(task, retries=2, threshold=0.7):
    attempt = 0
    while attempt <= retries:
        result, confidence, agent_used = agent.handle_task(task)
        print(f"   🔁 Attempt #{attempt+1} | Confidence: {confidence:.2f}")
        if confidence >= threshold:
            print(f"   ✅ Accepted: {result}")
            task_log.log(task, result, confidence, success=True)
            journal.record(task, result, agent_used, confidence)  # ✅ Log agent usage
            return
        else:
            print("   ⚠️ Retry due to low confidence...")
            attempt += 1

    print("   🌐 WebAgent fallback activated...")
    hint = agent.web_agent.fetch_insight(task)
    result, confidence, agent_used = agent.handle_task(task, injected_hint=hint)

    if confidence >= threshold:
        print(f"   ✅ Accepted (Web): {result}")
        task_log.log(task, result, confidence, success=True)
    else:
        print("   ❌ Failed after WebAgent. Logging fallback.")
        task_log.log(task, "Fallback after retries + Web", confidence, success=False)

    journal.record(task, result, agent_used, confidence)


def execute_goal(goal):
    print(f"\n🚀 High-Level Goal: {goal}")
    subtasks = planner.generate_task_tree(goal)
    print(f"🧩 Generated {len(subtasks)} Subtasks:\n")

    for i, task in enumerate(subtasks, 1):
        print(f"🔹 Task {i}/{len(subtasks)}: {task}")
        execute_with_retries(task)

    print("\n📊 Final Summary for Goal:")
    task_log.print_summary()

    print("\n📘 Journal Entries:")
    journal.print_log()


if __name__ == "__main__":
    goals = [
        "Launch Instagram campaign for Ganesh Chaturthi",
        "Plan YouTube series on AI tools for students",
    ]

    for goal in goals:
        execute_goal(goal)
