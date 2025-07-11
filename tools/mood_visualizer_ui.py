from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import streamlit as st
from memory.agent_memory import AgentMemory
import matplotlib.pyplot as plt

MOOD_SCALE = {"stable": 1, "anxious": 2, "overwhelmed": 3}

st.title("📈 Agent Mood Tracker")

mem = AgentMemory()
agent_names = list(mem.memory.keys())
agent = st.selectbox("Select Agent", agent_names)

entries = mem.get_memory(agent, filter_by_type="thought")
mood_entries = [e for e in entries if "mood" in e["task"]]

if mood_entries:
    labels = [e["timestamp"][-8:] for e in mood_entries]
    moods = [
        MOOD_SCALE.get(e["content"].split(": ")[-1].lower(), 1) for e in mood_entries
    ]

    fig, ax = plt.subplots()
    ax.plot(labels, moods, marker="o")
    ax.set_yticks([1, 2, 3])
    ax.set_yticklabels(["Stable", "Anxious", "Overwhelmed"])
    ax.set_title(f"{agent}'s Mood Over Time")
    ax.set_xlabel("Time")
    ax.set_ylabel("Mood State")

    st.pyplot(fig)
else:
    st.warning("No mood updates found for this agent.")
