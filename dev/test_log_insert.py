from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
import sqlite3
import os
from datetime import datetime

# Correct DB path
DB_PATH = os.path.join("dashboard", "db", "task_logs.db")

# Insert dummy log
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute(
    """
    INSERT INTO logs (timestamp, task, agent, confidence, final_result)
    VALUES (?, ?, ?, ?, ?)
""",
    (
        datetime.now().isoformat(),
        "Test: What's the weather today?",
        "WeatherAgent",
        0.92,
        "The weather today is sunny with a high of 33°C.",
    ),
)

conn.commit()
conn.close()

print("✅ Dummy log inserted.")
