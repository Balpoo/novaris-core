from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods

# memory/journal.py

import json
from datetime import datetime
import os


class ActionJournal:
    def __init__(self, path="memory/journal_log.json"):
        self.path = path
        if os.path.exists(self.path):
            with open(self.path, "r") as f:
                self.entries = json.load(f)
        else:
            self.entries = []

    def record(self, task, result, agent_name, confidence):
        entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "task": task,
            "agent": agent_name,
            "confidence": confidence,
            "result": result,
        }
        self.entries.append(entry)
        self._save()

    def _save(self):
        with open(self.path, "w") as f:
            json.dump(self.entries, f, indent=2)

    def print_log(self):
        print("\n📘 NOVARIS Action Journal")
        for entry in self.entries[-10:]:
            print(
                f"🕒 {entry['timestamp']} | {entry['agent']} → {entry['task']} ({entry['confidence']})"
            )
