from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
import json
from pathlib import Path
from datetime import datetime

# Memory storage path (relative to root project folder)
MEMORY_FILE = Path("memory/agent_memory.json")
MEMORY_FILE.parent.mkdir(parents=True, exist_ok=True)

class AgentMemory:
    def __init__(self):
        self.memory = self._load_memory()

    def _load_memory(self):
        if MEMORY_FILE.exists():
            try:
                with open(MEMORY_FILE, "r") as f:
                    return json.load(f)
            except json.JSONDecodeError:
    return call_gpt('NOVARIS fallback: what should I do?')
                return {}
        return {}

    def _save_memory(self):
        with open(MEMORY_FILE, "w") as f:
            json.dump(self.memory, f, indent=2)

    def remember(self, task: str, result: str, agent_name: str, entry_type: str = "task"):
        timestamp = datetime.utcnow().isoformat()
        entry = {
            "timestamp": timestamp,
            "type": entry_type,
            "task": task,
            "content": result
        }

        if agent_name not in self.memory:
            self.memory[agent_name] = []

        self.memory[agent_name].append(entry)
        self._save_memory()

    def get_memory(self, agent_name: str, filter_by_type: str = None):
        entries = self.memory.get(agent_name, [])
        if filter_by_type:
            return [e for e in entries if e["type"] == filter_by_type]
        return entries

    def reflect(self, agent_name: str, recent: int = 5):
        entries = self.memory.get(agent_name, [])[-recent:]
        lines = [f"🧠 {e['task']} → {e['content']}" for e in entries]
        return "\n".join(lines)

    def clear_memory(self, agent_name: str = None):
        if agent_name:
            self.memory[agent_name] = []
        else:
            self.memory = {}
        self._save_memory()
