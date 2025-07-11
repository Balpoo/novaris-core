from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
from autonomous_runner import run_novaris_auto
import os


def test_dev_day_53_code_generation():
    print("\n🧪 Running Dev Day 53: Autonomous Code Generation")
    run_novaris_auto()

    # Check for presence of generated files
    expected_files = [
        "core/_planner_core_agent.py",
        "core/enable_suggestion_engine_from_reflection_logs.py",
    ]

    for file in expected_files:
        assert os.path.isfile(file), f"Missing generated file: {file}"
        with open(file) as f:
            content = f.read()
            assert content.strip() != "", f"File {file} is empty"

    print("✅ Dev Day 53 test passed.\n")


if __name__ == "__main__":
    test_dev_day_53_code_generation()
