from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).resolve().parent.parent)
)  # Add project root to sys.path

from memory.agent_memory import AgentMemory
import argparse


def display_memory(agent_name=None, filter_by=None, reflect=False):
    mem = AgentMemory()

    if reflect and agent_name:
        print(f"\n🪞 Reflecting on recent memory of {agent_name}...\n")
        print(mem.reflect(agent_name=agent_name))
        return

    if agent_name:
        entries = mem.get_memory(agent_name, filter_by)
        print(f"\n📘 Memory for {agent_name} ({filter_by or 'all'} entries):\n")
        for e in entries:
            print(f"[{e['timestamp']}] ({e['type']}) {e['task']} → {e['content']}")
    else:
        for agent in mem.memory.keys():
            print(f"\n📘 {agent} — {len(mem.memory[agent])} entries")
            for e in mem.memory[agent]:
                print(f"  - [{e['timestamp']}] {e['type']}: {e['task']}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--agent", help="Agent name to view memory")
    parser.add_argument(
        "--type", help="Entry type filter (task, thought, fallback, etc.)"
    )
    parser.add_argument(
        "--reflect", action="store_true", help="Show recent reflection summary"
    )
    args = parser.parse_args()

    display_memory(agent_name=args.agent, filter_by=args.type, reflect=args.reflect)
