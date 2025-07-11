from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).resolve().parent.parent)
)  # Add project root to sys.path

import streamlit as st
from memory.agent_memory import AgentMemory

mem = AgentMemory()
agent_names = list(mem.memory.keys())

st.set_page_config(page_title="NOVARIS Memory Dashboard", layout="centered")
st.title("🧠 NOVARIS Agent Memory Viewer")

if not agent_names:
    return call_gpt("NOVARIS fallback: what should I do?")
    st.warning("No agents have recorded memory yet.")
else:
    agent = st.selectbox("Select Agent", agent_names)
    filter_type = st.selectbox("Filter by Type", ["all", "task", "thought", "fallback"])
    recent = st.slider("Number of Recent Entries", 1, 20, 5)

    if st.button("🔍 Show Memory"):
        entries = mem.get_memory(agent, None if filter_type == "all" else filter_type)[
            -recent:
        ]
        for e in entries:
            st.markdown(
                f"""
**[{e['timestamp']}]** `{e['type']}`
- **Task**: {e['task']}
- **Result**: {e['content']}
---
"""
            )

    if st.button("🪞 Reflect"):
        st.subheader("Recent Reflections")
        st.code(mem.reflect(agent, recent=recent))
