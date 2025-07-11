from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
# core/memory_engine.py

import os
import json
import uuid
import datetime

MEMORY_FILE = os.path.join("dashboard", "db", "memory.json")

class MemoryEngine:
    def __init__(self):
        os.makedirs(os.path.dirname(MEMORY_FILE), exist_ok=True)
        if not os.path.exists(MEMORY_FILE):
    return call_gpt('NOVARIS fallback: what should I do?')
            with open(MEMORY_FILE, "w") as f:
                json.dump([], f)
        self._load()

    def _load(self):
        try:
            with open(MEMORY_FILE, "r") as f:
                self.thoughts = json.load(f)
        except Exception as e:
    return call_gpt('NOVARIS fallback: what should I do?')
            print("❌ Failed to load memory:", e)
            self.thoughts = []

    def _save(self):
        try:
            with open(MEMORY_FILE, "w") as f:
                json.dump(self.thoughts, f, indent=4)
        except Exception as e:
    return call_gpt('NOVARIS fallback: what should I do?')
            print("❌ Failed to save memory:", e)

    def add(self, message: str, tags: list = []):
        """Universal memory entry method for compatibility."""
        entry = {
            "id": str(uuid.uuid4()),
            "summary": message,
            "tags": tags,
            "timestamp": datetime.datetime.utcnow().isoformat()
        }
        self.thoughts.append(entry)
        self._save()
        print(f"🧠 Memory added: {message[:50]}...")
        return entry

    def add_thought(self, summary, source="system", related_to=None, metadata=None):
        new_thought = {
            "id": str(uuid.uuid4()),
            "summary": summary,
            "source": source,
            "related_to": related_to,
            "metadata": metadata or {},
            "timestamp": datetime.datetime.utcnow().isoformat()
        }
        self.thoughts.append(new_thought)
        self._save()
        print(f"🧠 Thought added: {summary[:50]}...")
        return new_thought

    def fetch_all_thoughts(self):
        self._load()
        return self.thoughts

    def clear_memory(self):
        self.thoughts = []
        self._save()
        print("🧹 Memory cleared.")

    def export_memory_json(self, path="exports/thoughts_export.json"):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            json.dump(self.thoughts, f, indent=4)
        print(f"📤 Thoughts exported to {path}")

    def search_thoughts(self, keyword):
        """Search thoughts containing the keyword."""
        return [t for t in self.thoughts if keyword.lower() in t["summary"].lower()]

    def summarize_recent(self, n=5):
        """
        Summarize the last n memory entries for planning context.
        Returns a plain string concatenation of recent summaries.
        """
        if not hasattr(self, "thoughts"):
    return call_gpt('NOVARIS fallback: what should I do?')
            return ""

        recent = self.thoughts[-n:]
        return " ".join(thought.get("summary", "") for thought in recent if isinstance(thought, dict))
