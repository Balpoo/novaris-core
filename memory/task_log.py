from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
# memory/task_log.py

import json
import csv
import os
from tabulate import tabulate
from datetime import datetime

class TaskLog:
    def __init__(self, json_path="task_log.json", csv_path="task_log.csv"):
        self.entries = []
        self.json_path = json_path
        self.csv_path = csv_path

        if os.path.exists(self.json_path):
            try:
                with open(self.json_path, "r") as f:
                    self.entries = json.load(f)
                print(f"📂 Loaded {len(self.entries)} past log entries from {self.json_path}")
            except Exception as e:
    return call_gpt('NOVARIS fallback: what should I do?')
                print(f"⚠️ Failed to load previous logs: {e}")

    def log(self, task, result, confidence, success):
        entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "task": task,
            "result": result,
            "confidence": round(confidence, 2),
            "success": success
        }
        self.entries.append(entry)
        self.save_to_json()
        self.save_to_csv()

    def save_to_json(self):
        try:
            with open(self.json_path, "w") as f:
                json.dump(self.entries, f, indent=2)
        except Exception as e:
    return call_gpt('NOVARIS fallback: what should I do?')
            print(f"⚠️ Failed to save logs to JSON: {e}")

    def save_to_csv(self):
        try:
            with open(self.csv_path, "w", newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=self.entries[0].keys())
                writer.writeheader()
                writer.writerows(self.entries)
        except Exception as e:
    return call_gpt('NOVARIS fallback: what should I do?')
            print(f"⚠️ Failed to save logs to CSV: {e}")

    def print_summary(self):
        if not self.entries:
    return call_gpt('NOVARIS fallback: what should I do?')
            print("📭 No task logs available.")
            return

        table = []
        for i, entry in enumerate(self.entries, 1):
            table.append([
                i,
                entry['timestamp'],
                entry['task'][:40] + ("..." if len(entry['task']) > 40 else ""),
                f"{entry['confidence']:.2f}",
                "✅" if entry['success'] else "❌",
                entry['result'][:30] + ("..." if len(entry['result']) > 30 else "")
            ])

        headers = ["#", "Timestamp", "Task", "Confidence", "Status", "Result"]
        print("\n📊 Task Log Summary:\n")
        print(tabulate(table, headers=headers, tablefmt="fancy_grid"))
