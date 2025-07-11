from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
from core.agent_registry import AgentRegistry
from core.reflection_engine import reflect_on_day


def test_dev_day_48():
    print("\n🧪 NOVARIS Self-Growth Test — Dev Day 48")

    registry = AgentRegistry()

    # 1. Register and update core agent — keep it forever
    registry.register(
        "reflection", "Self-Learning", "Logs and reflects on each dev day."
    )
    registry.update_status("reflection", "active")

    # 2. Register and cleanup dummy test agent
    registry.register(
        "test_dummy", "Temporary Test", "Used only for registration test."
    )
    registry.update_status("test_dummy", "testing")
    print("📦 Dummy Agent Snapshot:", registry.get("test_dummy"))
    registry.unregister("test_dummy")

    # 3. Inject Reflection Log (permanent log entry)
    reflect_on_day(
        dev_day=48,
        what_was_done="Initialized Agent Registry, Folder Mapper, and Reflection Engine. NOVARIS brain begins today.",
        next_steps="Begin Planner Core, Voice Trigger, and Agent Collaboration by Dev Day 50.",
    )

    print("✅ Dev Day 48 Self-Growth Test Completed.\n")


if __name__ == "__main__":
    test_dev_day_48()
