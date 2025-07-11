from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods

# ✅ tests/main.py

from core.reflection_engine import reflect_on_day
from core.agent_registry import AgentRegistry
from core.planner import suggest_next_dev_day
from core.voice_agent import speak_plan

if __name__ == "__main__":
    print("\n🔁 Running NOVARIS Dev Day Injection Sequence...\n")

    # === Dev Day 48 Memory Injection ===
    reflect_on_day(
        dev_day=48,
        what_was_done="Initialized Agent Registry, Folder Mapper, and Reflection Engine. NOVARIS brain begins today.",
        next_steps="Begin Planner Core, Voice Trigger, and Agent Collaboration by Dev Day 50.",
    )

    # === Register Core Agents ===
    registry = AgentRegistry()
    registry.register(
        "reflection", "Self-Learning", "Logs and reflects on each dev day."
    )
    registry.update_status("reflection", "active")

    # === Dev Day 49 Plan Generation ===
    plan_49 = suggest_next_dev_day()
    if plan_49:
        print(f"\n✅ Planner injected Dev Day {plan_49['dev_day']}")
        for task in plan_49["suggested_tasks"]:
            print("🧩", task)

    # === Dev Day 50 Memory Injection ===
    reflect_on_day(
        dev_day=50,
        what_was_done="Voice Agent activated. NOVARIS now speaks from its planner log using offline TTS.",
        next_steps="Enable agent collaboration logic. Connect planner → executor → reflection.",
    )

    # === Dev Day 51 Collaboration Logic Activated ===
    reflect_on_day(
        dev_day=51,
        what_was_done="Executor Agent created. Agent Collaborator routes planner tasks to executor and logs results to reflection.",
        next_steps="Add trust score, retry mechanism, and fallback logic for executor failures.",
    )

    # === Dev Day 51 Plan Generation ===
    plan_51 = suggest_next_dev_day()
    if plan_51:
        print(f"\n✅ Planner injected Dev Day {plan_51['dev_day']}")
        for task in plan_51["suggested_tasks"]:
            print("🧩", task)

    # === Dev Day 51 Voice Agent Trigger ===
    print("\n🔊 Triggering NOVARIS Voice Agent...\n")
    speak_plan(51)

    # === Dev Day 52 Memory Injection ===
    reflect_on_day(
        dev_day=52,
        what_was_done="Enabled trust logic, retry mechanism, and autonomous task execution with planner → executor → reflection loop.",
        next_steps="Allow NOVARIS to generate new agent code from planner descriptions (Dev Day 53+).",
    )

    plan_52 = suggest_next_dev_day()
    if plan_52:
        print(f"\n✅ Planner injected Dev Day {plan_52['dev_day']}")
        for task in plan_52["suggested_tasks"]:
            print("🧩", task)

    print("\n🔊 Triggering NOVARIS Voice Agent...\n")
    speak_plan(52)

    # === Dev Day 53 Memory Injection ===
    reflect_on_day(
        dev_day=53,
        what_was_done="Autonomous code generation engine created and modules generated.",
        next_steps="Enable code self-validation and syntax checking.",
    )

    plan_53 = suggest_next_dev_day()
    if plan_53:
        print(f"\n✅ Planner injected Dev Day {plan_53['dev_day']}")
        for task in plan_53["suggested_tasks"]:
            print("🧩", task)

    # === Dev Day 54 Memory Injection ===
    reflect_on_day(
        dev_day=54,
        what_was_done="Planner and executor tasks executed with trust and retry.",
        next_steps="Refine collaboration logic and logging.",
    )

    # === Dev Day 55 Memory Injection ===
    reflect_on_day(
        dev_day=55,
        what_was_done="Extended code generation across multiple modules autonomously.",
        next_steps="Add code quality and syntax checks.",
    )

    print("\n✅ Memory + Agent + Planner + Voice Injection Complete.\n")
