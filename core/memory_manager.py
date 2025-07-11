from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
import json
from datetime import datetime
from pathlib import Path

MEMORY_FILE = Path("memory/agent_memory.json")
MEMORY_FILE.parent.mkdir(exist_ok=True)


class MemoryManager:
    def __init__(self):
        self.memory = self._load_memory()

    def _load_memory(self):
        if MEMORY_FILE.exists():
            with open(MEMORY_FILE, "r") as f:
                return json.load(f)
        return {}

    def _save_memory(self):
        with open(MEMORY_FILE, "w") as f:
            json.dump(self.memory, f, indent=2)

    def log(self, agent_name, content, entry_type="note"):
        timestamp = datetime.utcnow().isoformat()
        entry = {"timestamp": timestamp, "type": entry_type, "content": content}
        self.memory.setdefault(agent_name, []).append(entry)
        self._save_memory()

    def get_memory(self, agent_name):
        return self.memory.get(agent_name, [])

    def clear_memory(self, agent_name=None):
        if agent_name:
            self.memory[agent_name] = []
        else:
            self.memory = {}
        self._save_memory()
