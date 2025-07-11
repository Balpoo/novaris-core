from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods

# ✅ tests/dev_day_52_test.py

from autonomous_runner import run_novaris_auto


def test_dev_day_52_autonomy():
    print("\n🧪 Running Dev Day 52: Autonomous Planning & Execution")
    run_novaris_auto()
    print("✅ Dev Day 52 test passed.\n")


if __name__ == "__main__":
    test_dev_day_52_autonomy()
