from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
import csv
from retry_insights import get_retry_filtered


def export_retry_logs_to_csv(filepath="exports/retry_logs_export.csv", min_retries=1):
    logs = get_retry_filtered(min_retries=min_retries)
    with open(filepath, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Task", "Result", "Status", "Retry Count", "Timestamp"])
        for row in logs:
            writer.writerow(row)
    return filepath
