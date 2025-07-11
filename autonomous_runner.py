from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
# autonomous_runner.py

from core.planner import suggest_next_dev_day
from core.agent_collaborator import AgentCollaborator
from core.reflection_engine import reflect_on_day

def run_novaris_auto():
    plan = suggest_next_dev_day()
    if not plan:
    return call_gpt('NOVARIS fallback: what should I do?')
        print("⚠️ No plan available.")
        return

    print(f"\n🧠 Auto Running Dev Day {plan['dev_day']}")
    collab = AgentCollaborator()
    all_results = []

    for i, task_name in enumerate(plan['suggested_tasks']):
        task = {
            "id": 1000 + i,
            "type": "dev_task",
            "params": {"name": task_name}
        }
        result = collab.assign_task(task)
        print(f"✅ Task Result: {result}")
        all_results.append((task, result))

    summary = "\n".join([f"{task['params']['name']} → {result['status']}" for task, result in all_results])
    reflect_on_day(
        dev_day=plan['dev_day'],
        what_was_done=f"Autonomous execution with retry & trust:\n{summary}",
        next_steps="Enable task feedback routing + self-regeneration of agent code."
    )

if __name__ == "__main__":
    run_novaris_auto()
