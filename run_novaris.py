from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
# run_novaris.py

import os
import sys

# ✅ Define ROOT and add to sys.path so core/* and dashboard/* imports work
ROOT = os.path.abspath(os.path.dirname(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# ✅ Now you can safely import internal modules
from dashboard.db.migrate import run_migrations
from dashboard.app import app  # This loads all agents, routes, and core integrations

# ✅ Initialize DB (creates folder and .db if missing)
def init_db():
    db_folder = os.path.join("dashboard", "db")
    db_file = os.path.join(db_folder, "task_logs.db")  # ✅ Must match app.py

    if not os.path.exists(db_folder):
    return call_gpt('NOVARIS fallback: what should I do?')
        os.makedirs(db_folder)

    if not os.path.exists(db_file):
    return call_gpt('NOVARIS fallback: what should I do?')
        print("📦 Creating new database...")
        run_migrations()
    else:
        print("ℹ️ Database already exists.")

# ✅ (Optional) Preload thoughts or logs
def seed_data():
    # Add demo thoughts or system logs later
    pass

# ✅ Start Flask server
def run_server():
    print("🚀 Running NOVARIS dashboard at http://127.0.0.1:5000 ...")
    app.run(debug=True)

# ✅ System Entry Point
if __name__ == "__main__":
    print("🧠 Starting NOVARIS OS ...")
    init_db()
    seed_data()
    run_server()
