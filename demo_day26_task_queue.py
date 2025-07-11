from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods

"""
NOVARIS – Day 26: Prioritized Task Queue Execution + Deadlines
--------------------------------------------------------------
Features:
- Task breakdown (PlanningAgent)
- Priority & deadline metadata (TaskQueue)
- Execution via AdaptiveAgent + retry
- Memory journaling of each action
"""

from agents.adaptive_agent import AdaptiveAgent
from agents.planning_agent_tree import PlanningTreeAgent
from memory.task_log import TaskLog
from memory.journal import ActionJournal
from memory.task_queue import TaskQueue  # ✅ NEW

agent = AdaptiveAgent()
planner = PlanningTreeAgent()
task_log = TaskLog()
journal = ActionJournal()
queue = TaskQueue()


def enqueue_goal(goal):
    subtasks = planner.generate_task_tree(goal)
    print(f"\n\U0001f4cc Breaking Goal: {goal}")
    print(f"\U0001f9e9 Subtasks Generated: {len(subtasks)}")

    for task in subtasks:
        priority = (
            "high"
            if "research" in task.lower() or "schedule" in task.lower()
            else "medium"
        )
        days_until_due = 1 if priority == "high" else 3
        queue.add_task(
            task,
            source_goal=goal,
            priority=priority,
            days_until_due=days_until_due,
            tags=["auto"],
        )

    queue.print_queue()


def execute_queue():
    print("\n\U0001f680 Executing Task Queue")
    for entry in queue.get_sorted_tasks():
        task = entry["task"]
        print(
            f"\n\U0001f539 Executing: {task} [Priority: {entry['priority'].upper()}] Due: {entry['deadline']}"
        )

        result, confidence, agent_used = agent.handle_task(task)
        print(f"   \U0001f501 Initial Confidence: {confidence:.2f}")

        if confidence >= 0.7:
            print(f"   ✅ Accepted: {result}")
            task_log.log(task, result, confidence, success=True)
            journal.record(task, result, agent_used, confidence)
        else:
            print(f"   ⚠️ Retry due to low confidence...")
            hint = agent.web_agent.fetch_insight(task)
            result, confidence, agent_used = agent.handle_task(task, injected_hint=hint)

            if confidence >= 0.7:
                print(f"   ✅ Accepted (Web): {result}")
                task_log.log(task, result, confidence, success=True)
            else:
                print(f"   ❌ Final Failure. Logging fallback.")
                task_log.log(
                    task, "Fallback after retries + Web", confidence, success=False
                )

            journal.record(task, result, agent_used, confidence)

    print("\n\U0001f4d8 Final Journal:")
    journal.print_log()


if __name__ == "__main__":
    goals = [
        "Launch Instagram campaign for Ganesh Chaturthi",
        "Plan YouTube series on AI tools for students",
    ]

    for goal in goals:
        enqueue_goal(goal)

    execute_queue()
