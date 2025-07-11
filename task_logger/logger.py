from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods

# task_logger/logger.py
import json
import os
from datetime import datetime

LOG_FILE_PATH = "logs/task_log.jsonl"


def ensure_log_path():
    os.makedirs(os.path.dirname(LOG_FILE_PATH), exist_ok=True)


def log_task(reflection_data: dict):
    ensure_log_path()
    with open(LOG_FILE_PATH, "a", encoding="utf-8") as f:
        json.dump({"timestamp": datetime.utcnow().isoformat(), **reflection_data}, f)
        f.write("\n")


def export_log_to_csv(csv_path="logs/task_log.csv"):
    import csv

    ensure_log_path()
    with open(LOG_FILE_PATH, "r", encoding="utf-8") as jsonl_file, open(
        csv_path, "w", newline="", encoding="utf-8"
    ) as csv_file:

        reader = (json.loads(line) for line in jsonl_file)
        first = next(reader, None)
        if first:
            writer = csv.DictWriter(csv_file, fieldnames=first.keys())
            writer.writeheader()
            writer.writerow(first)
            for row in reader:
                writer.writerow(row)

        # Optional CLI entry to export .csv


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Task Logger CLI")
    parser.add_argument("--export-csv", action="store_true", help="Export JSONL to CSV")

    args = parser.parse_args()
    if args.export_csv:
        export_log_to_csv()
        print("✅ Exported logs/task_log.csv")
