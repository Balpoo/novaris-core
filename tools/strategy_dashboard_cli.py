from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from memory.agent_memory import AgentMemory


def view_strategy(agent_name):
    mem = AgentMemory()
    entries = mem.get_memory(agent_name, filter_by_type="thought")
    print(f"\n🧠 Strategy + Coaching Log for {agent_name}:\n")
    for e in entries:
        if "strategy" in e["task"] or "self_coach" in e["task"]:
            print(f"[{e['timestamp']}] {e['task']} → {e['content']}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--agent", required=True)
    args = parser.parse_args()
    view_strategy(args.agent)
