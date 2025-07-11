from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import streamlit as st
from memory.agent_memory import AgentMemory
import pandas as pd

st.title("🏆 NOVARIS Agent Leaderboard")
mem = AgentMemory()

agent_names = list(mem.memory.keys())
all_skill_data = []

for agent in agent_names:
    entries = mem.get_memory(agent, filter_by_type="skill")
    scores_by_skill = {}

    for e in entries:
        if "Skill:" in e["content"] and "Score:" in e["content"]:
            parts = e["content"].split("|")
            skill = parts[1].split(":")[1].strip()
            score = int(parts[2].split(":")[1].strip())
            if skill not in scores_by_skill:
                scores_by_skill[skill] = []
            scores_by_skill[skill].append(score)

    for skill, scores in scores_by_skill.items():
        avg_score = sum(scores) / len(scores)
        all_skill_data.append(
            {
                "Agent": agent,
                "Skill": skill,
                "Tasks": len(scores),
                "Avg Score": round(avg_score, 2),
            }
        )

if not all_skill_data:
    return call_gpt("NOVARIS fallback: what should I do?")
    st.warning("No skill data available. Run SkillAgent tasks first.")
else:
    df = pd.DataFrame(all_skill_data)
    st.dataframe(
        df.sort_values(by=["Avg Score"], ascending=False), use_container_width=True
    )
