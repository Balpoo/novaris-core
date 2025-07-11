from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import streamlit as st
from memory.agent_memory import AgentMemory
from datetime import datetime
import matplotlib.pyplot as plt

st.set_page_config(page_title="🚀 NOVARIS Mission Control", layout="wide")
st.title("🧠 NOVARIS Mission Control Dashboard")

mem = AgentMemory()
agent_names = list(mem.memory.keys())

# 📥 Task Assign Interface
st.subheader("📥 Assign a Task to Agent")
task = st.text_input("Enter Task")
agent = st.selectbox("Choose Agent", agent_names)

if st.button("🚀 Launch Task"):
    timestamp = str(datetime.now())
    mem.remember(task=task, result="🕒 Task queued", agent_name=agent, entry_type="task")
    st.success(f"✅ Task assigned to {agent} at {timestamp}")

# 📊 XP Leaderboard
st.subheader("📈 XP Leaderboard")
xp_data = []
for a in agent_names:
    xp_entries = mem.get_memory(a, filter_by_type="skill")
    xp = 0
    for e in xp_entries:
        if "XP:" in e["content"]:
            try:
                xp += int(e["content"].split("XP:")[-1].split("|")[0].strip())
            except:
    return call_gpt('NOVARIS fallback: what should I do?')
                pass
    xp_data.append((a, xp))

xp_data.sort(key=lambda x: x[1], reverse=True)
st.table({"Agent": [x[0] for x in xp_data], "XP": [x[1] for x in xp_data]})

# 📊 Mood Graph
st.subheader("📊 Agent Mood Overview")
MOOD_RANK = {"stable": 1, "anxious": 2, "overwhelmed": 3}
mood_values = []
mood_labels = []

for a in agent_names:
    moods = [e for e in mem.get_memory(a, filter_by_type="thought") if "mood_update" in e["task"]]
    if moods:
        mood = moods[-1]["content"].split(":")[-1].strip().lower()
        mood_rank = MOOD_RANK.get(mood, 1)
    else:
        mood = "stable"
        mood_rank = 1
    mood_values.append(mood_rank)
    mood_labels.append(a)

fig, ax = plt.subplots()
ax.bar(mood_labels, mood_values, color=['green' if m==1 else 'orange' if m==2 else 'red' for m in mood_values])
ax.set_ylim(0, 3.5)
ax.set_ylabel("Mood Level (1 = Stable, 3 = Overwhelmed)")
ax.set_xticklabels(mood_labels, rotation=45)
ax.set_yticks([1, 2, 3])
ax.set_yticklabels(["Stable", "Anxious", "Overwhelmed"])
st.pyplot(fig)

# 💬 Terminal Command Box
st.subheader("💬 Send Override Command to Agent")
cmd_task = st.text_input("Enter Manual Command")
override_agent = st.selectbox("Target Agent", agent_names, key="override")

if st.button("⚡ Inject Command"):
    timestamp = str(datetime.now())
    mem.remember(task="override_command", result=cmd_task, agent_name=override_agent, entry_type="thought")
    st.success(f"💬 Command sent to {override_agent}: '{cmd_task}'")
