from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods

# ✅ tests/dev_day_50_test.py

from core.voice_agent import speak_plan


def test_voice_agent():
    print("\n🧪 NOVARIS Voice Agent Test — Dev Day 50")
    plan = speak_plan(49)  # You can change dev day here
    if plan:
        print("\n✅ Voice Agent successfully read planner log.")
    else:
        print("❌ Voice Agent failed to retrieve plan.")


if __name__ == "__main__":
    test_voice_agent()
