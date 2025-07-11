from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
from retry_logger import initialize_retry_column, update_retry_count
import sqlite3

DB_PATH = "dashboard/db/task_logs.db"


def list_available_ids():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT id, task, retry_count FROM task_logs")
    rows = cur.fetchall()
    conn.close()
    print("\n🗂 Available Tasks in DB:")
    for row in rows:
        print(f"   ID: {row[0]} | Task: {row[1]} | Retries: {row[2]}")
    print("-" * 40)


def fetch_retry_count(task_id):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT retry_count FROM task_logs WHERE id = ?", (task_id,))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else None


def test_retry_flow(task_id):
    print("🔧 Running retry logger test...")

    initialize_retry_column()
    print("✅ Column checked/created.")

    before = fetch_retry_count(task_id)
    print(f"📊 Retry count BEFORE: {before}")

    update_retry_count(task_id)

    after = fetch_retry_count(task_id)
    print(f"✅ Retry count AFTER: {after}")


if __name__ == "__main__":
    list_available_ids()
    test_id = int(input("Enter test task ID to retry: "))
    test_retry_flow(test_id)
