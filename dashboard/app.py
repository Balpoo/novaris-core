from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
from core.reflection_engine import get_last_reflection_time

from flask import Flask, render_template, flash
import sys
import os
import sqlite3  # ✅ Needed for DB log loading

# ✅ Add project root so 'core' and others are importable
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# ✅ Run DB migrations
from dashboard.db.migrate import run_migrations
run_migrations()

# ✅ Flask & Blueprints
from dashboard.routes.filters import filters_bp
from dashboard.routes.backup import backup_bp
from dashboard.routes.export import export_bp
from dashboard.routes.reflections import reflections_bp
from dashboard.routes.file_browser import file_browser_bp
from dashboard.routes.scheduler import scheduler_bp  # ✅ Scheduler added
from dashboard.routes.retry import retry_bp
from dashboard.routes.logs import logs_bp
from dashboard.routes.csve_routes import csve_bp  # ✅ New CSVE route
from dashboard.routes.csve_save import csve_save_bp
from dashboard.routes.gdrive_upload import gdrive

# ✅ Init Flask app
app = Flask(__name__)
app.secret_key = "novaris_secret_2047"  # Used for flash messages

# ✅ Register Blueprints
app.register_blueprint(filters_bp)
app.register_blueprint(backup_bp)
app.register_blueprint(export_bp)
app.register_blueprint(reflections_bp)
app.register_blueprint(file_browser_bp)
app.register_blueprint(scheduler_bp)  # ✅ Scheduler UI route registered
app.register_blueprint(retry_bp)
app.register_blueprint(logs_bp)
app.register_blueprint(csve_bp)  # ✅ Register CSVE validation route
app.register_blueprint(csve_save_bp)
app.register_blueprint(gdrive)

# ✅ DB Path
DB_PATH = os.path.join(os.path.dirname(__file__), "db", "task_logs.db")

# ✅ Load logs for home dashboard
def load_logs():
    logs = []
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("""
            SELECT timestamp, task, agent, confidence, final_result
            FROM logs
            ORDER BY timestamp DESC
            LIMIT 100
        """)
        logs = [dict(row) for row in cursor.fetchall()]
        conn.close()
    except Exception as e:
    return call_gpt('NOVARIS fallback: what should I do?')
        print("❌ Failed to load logs:", e)
    return logs

# ✅ Home route
@app.route("/")
def index():
    logs = load_logs()
    last_reflected = get_last_reflection_time()
    return render_template("index.html", logs=logs, last_reflected=last_reflected)

# ✅ Background Agents
from dashboard.agent_runner import start_all_agents
start_all_agents()

# ✅ Scheduler Engine
from dashboard.scheduler_engine import start_scheduler_engine
start_scheduler_engine()

# ✅ Retry Engine
from dashboard.retry_engine import start_retry_engine
start_retry_engine()

# ✅ Launch server (only if run directly, not when imported)
if __name__ == "__main__":
    app.run(debug=True)
