from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods

# auto_loop_agent.py

import argparse
from reflection.reflection_engine import ReflectionEngine
from memory.reflective_memory import ReflectiveMemory
from task_logger.logger import export_log_to_csv
from task_logger.dashboard_ui import show_dashboard


def run_loop():
    memory = ReflectiveMemory()
    engine = ReflectionEngine(memory)

    print(
        "🧠 NOVARIS Auto Agent Loop is live.\nType your task below (or type 'exit'):\n"
    )

    while True:
        task = input("📝 Task → ")

        if task.strip().lower() == "exit":
            print("\n👋 Exiting NOVARIS. See you next session, Commander.")
            break

        print(f"\n🔍 Processing: '{task}'\n")

        reflection = engine.reflect_on_task(task)

        print("📋 Reflection Result:")
        for key, value in reflection.items():
            print(f"   {key}: {value}")

        print("\n" + "-" * 50 + "\n")


def main():
    parser = argparse.ArgumentParser(description="NOVARIS Auto Agent Loop")
    parser.add_argument(
        "--export-csv", action="store_true", help="📤 Export JSONL logs to CSV"
    )
    parser.add_argument(
        "--dashboard", action="store_true", help="📊 Launch Task Memory Dashboard"
    )

    args = parser.parse_args()

    if args.export_csv:
        export_log_to_csv()
        print("✅ Logs exported to logs/task_log.csv")

    elif args.dashboard:
        show_dashboard()

    else:
        run_loop()


if __name__ == "__main__":
    main()
