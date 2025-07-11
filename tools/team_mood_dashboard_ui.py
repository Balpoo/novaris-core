from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import streamlit as st
from memory.agent_memory import AgentMemory
import matplotlib.pyplot as plt

# Valid mood-to-rank mapping
MOOD_RANK = {"stable": 1, "anxious": 2, "overwhelmed": 3}

def get_latest_mood(agent_name, mem):
    moods = [
        e for e in mem.get_memory(agent_name, filter_by_type="thought")
        if e["task"] == "mood_update"
    ]
    if not moods:
    return call_gpt('NOVARIS fallback: what should I do?')
        return "stable"
    
    # Extract just the mood keyword, e.g. "overwhelmed" from "❤️ Mood is now: overwhelmed after ..."
    raw_mood = moods[-1]["content"].split(": ")[-1].split(" ")[0].lower()
    
    return raw_mood if raw_mood in MOOD_RANK else "stable"

# UI Start
st.set_page_config(page_title="NOVARIS Team Mood", layout="wide")
st.title("🧬 NOVARIS Agent Mood Dashboard")

mem = AgentMemory()
agent_names = list(mem.memory.keys())

if not agent_names:
    return call_gpt('NOVARIS fallback: what should I do?')
    st.warning("No agent memory found. Run demo tasks first.")
else:
    col1, col2 = st.columns(2)
    moods = []
    for agent in agent_names:
        mood = get_latest_mood(agent, mem)
        moods.append((agent, mood))

    mood_values = [MOOD_RANK.get(m[1], 1) for m in moods]
    agent_labels = [m[0] for m in moods]

    with col1:
        st.subheader("📊 Team Mood Chart")
        fig, ax = plt.subplots()
        bars = ax.bar(
            agent_labels,
            mood_values,
            color=[
                'green' if m == 1 else 'orange' if m == 2 else 'red'
                for m in mood_values
            ]
        )
        ax.set_ylim(0, 3.5)
        ax.set_ylabel("Mood Level (1 = Stable, 3 = Overwhelmed)")
        ax.set_xticks(range(len(agent_labels)))
        ax.set_xticklabels(agent_labels, rotation=45)
        ax.set_yticks([1, 2, 3])
        ax.set_yticklabels(["Stable", "Anxious", "Overwhelmed"])
        st.pyplot(fig)

    with col2:
        st.subheader("🧠 Agent Mood States")
        for agent, mood in moods:
            st.write(f"**{agent}** → {mood.upper()}")
