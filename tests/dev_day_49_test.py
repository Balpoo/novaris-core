from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
from core.planner import suggest_next_dev_day


def test_planner_suggestion():
    print("\n🧪 NOVARIS Planning Engine Test — Dev Day 49")

    suggestion = suggest_next_dev_day()
    if suggestion:
        print("🧩 Suggested Plan:")
        for task in suggestion["suggested_tasks"]:
            print("➡️", task)
    else:
        print("⚠️ Could not generate planner output. Check reflection logs.")


if __name__ == "__main__":
    test_planner_suggestion()
