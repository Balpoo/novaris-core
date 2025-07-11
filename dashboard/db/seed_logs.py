from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods

# dashboard/db/seed_logs.py

import sqlite3
import random
from datetime import datetime, timedelta
import os

# Correct paths
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DB_PATH = os.path.join(BASE_DIR, "db", "task_log.db")  # ✅ fixed
# BACKUP_SCRIPT = os.path.join(BASE_DIR, "utils", "backup.py")  # optional

statuses = ["pending", "done", "error", "retry"]
types = ["memory", "file", "agent", "system"]
agents = ["memory_agent", "file_agent", "planning_agent", "system"]
results = [
    "Task completed successfully.",
    "Error encountered during processing.",
    "Partial result saved.",
    "Agent rerouted the task.",
    "Log updated with memory result.",
]


def seed_logs():
    print("🌱 Seeding logs into SQLite...")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    for i in range(50):
        timestamp = datetime.now() - timedelta(
            days=random.randint(0, 10), hours=random.randint(0, 12)
        )
        task = f"Task #{i+1} - Simulated NOVARIS operation"
        status = random.choice(statuses)
        task_type = random.choice(types)
        agent = random.choice(agents)
        confidence = round(random.uniform(0.70, 0.99), 2)
        final_result = random.choice(results)

        cursor.execute(
            """
            INSERT INTO logs (timestamp, task, status, task_type, agent, confidence, final_result)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
            (
                timestamp.isoformat(),
                task,
                status,
                task_type,
                agent,
                confidence,
                final_result,
            ),
        )

    conn.commit()
    conn.close()
    print("✅ Inserted 50 dummy log entries.")

    # Optional backup trigger (disable unless implemented)
    # print("💾 Creating secure backup...")
    # try:
    #     subprocess.run(["python", BACKUP_SCRIPT], check=True)
    #     print("✅ Encrypted .7z backup created.")
    # except subprocess.CalledProcessError:
    #     print("❌ Backup script failed.")


if __name__ == "__main__":
    seed_logs()
