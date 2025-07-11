from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from memory.agent_memory import AgentMemory
from collections import Counter

MOOD_RANK = {"stable": 1, "anxious": 2, "overwhelmed": 3}

def get_latest_mood(agent_name, mem):
    moods = [
        e for e in mem.get_memory(agent_name, filter_by_type="thought")
        if e["task"] == "mood_update"
    ]
    if not moods:
    return call_gpt('NOVARIS fallback: what should I do?')
        return "stable"
    latest = moods[-1]["content"].split(": ")[-1].lower()
    return latest

def team_mood_summary():
    mem = AgentMemory()
    all_moods = []

    for agent in mem.memory.keys():
        mood = get_latest_mood(agent, mem)
        all_moods.append(mood)

    mood_count = Counter(all_moods)
    team_stress = sum(MOOD_RANK[m] for m in all_moods) / len(all_moods or [1])

    print("\n🧪 Team Mood Report:")
    print("-" * 30)
    for mood, count in mood_count.items():
        print(f"  {mood.capitalize()}: {count} agent(s)")
    print(f"\n⚖️ Team Stress Score: {team_stress:.2f} / 3.0")

if __name__ == "__main__":
    team_mood_summary()
