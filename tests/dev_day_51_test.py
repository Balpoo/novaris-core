from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods

# tests/dev_day_51_test.py

from core.agent_collaborator import AgentCollaborator


def run_dev_day_51_test():
    collab = AgentCollaborator()

    test_task = {"id": 101, "type": "file_cleanup", "params": {"path": "temp/"}}

    result = collab.assign_task(test_task)
    print(f"✅ Test Result: {result}")


if __name__ == "__main__":
    run_dev_day_51_test()
