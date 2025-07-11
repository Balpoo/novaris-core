from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods

# run_dashboard.py

from agents.planning_engine import PlanningEngine
from agents.task_executor import TaskExecutor

if __name__ == "__main__":
    planner = PlanningEngine()
    executor = TaskExecutor()

    task = input("Enter master task: ")
    steps = planner.decompose(task)

    print("\n📋 Task Plan:")
    for i, s in enumerate(steps, 1):
        print(f"{i}. {s}")

    confirm = input("\nRun all steps now? (y/n): ").lower()
    if confirm == "y":
        executor.execute_all(steps)
    else:
        print("❌ Execution cancelled.")
