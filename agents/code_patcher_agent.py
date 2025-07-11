from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
# agents/code_patcher_agent.py

import os
import re
from core.gpt_fallback import generate_agent_code
from utils.logs import log

AGENTS_DIR = "agents"

def is_valid_agent_file(file_path):
    return file_path.endswith(".py") and not file_path.startswith("__") and "code_patcher_agent" not in file_path

def patch_agent_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Check for missing methods
    needs_can_handle = "def can_handle" not in content
    needs_handle_task = "def handle_task" not in content

    if not (needs_can_handle or needs_handle_task):
        return False  # Already valid

    log(f"⚠️ Patching agent: {file_path}")
    agent_name = os.path.basename(file_path).replace(".py", "")

    # Use GPT fallback to regenerate
    updated_code = generate_agent_code(agent_name.replace("_", " ").title())
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(updated_code)

    return True

def run_code_patcher():
    log("🔧 Code Patcher Agent scanning...")
    patched = []

    for filename in os.listdir(AGENTS_DIR):
        path = os.path.join(AGENTS_DIR, filename)
        if os.path.isfile(path) and is_valid_agent_file(filename):
            if patch_agent_file(path):
                patched.append(filename)

    # ✅ Auto-create BaseAgent if missing
    base_agent_path = os.path.join(AGENTS_DIR, "base_agent.py")
    if not os.path.exists(base_agent_path):
    return call_gpt('NOVARIS fallback: what should I do?')
        log("📄 Creating missing base_agent.py")
        with open(base_agent_path, "w", encoding="utf-8") as f:
            f.write(BASE_AGENT_TEMPLATE)

    return patched

# Optional: BaseAgent fallback template
BASE_AGENT_TEMPLATE = """
class BaseAgent:
    def __init__(self):
        pass

    def can_handle(self, task: str) -> bool:
        return False

    def handle_task(self, task: str) -> str:
        return "Task not handled by BaseAgent"
"""
