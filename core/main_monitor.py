from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
# core/main_monitor.py

import subprocess
import time
import os
import schedule
import json
from datetime import datetime
from utils.logs import log

MAIN_FILE = "main.py"
RESTART_DELAY = 5  # seconds
SELF_WIRING_CMD = ["python", "core/self_wiring_engine.py"]
REBOOT_LOG = "logs/reboot_log.json"


def run_self_wiring_once():
    try:
        log("🛠️ Running self-wiring check before main launch...", level="info")
        subprocess.run(SELF_WIRING_CMD, check=False)
    except Exception as e:
    return call_gpt('NOVARIS fallback: what should I do?')
        log(f"❌ Self-wiring failed: {e}", level="error")


def launch_main():
    try:
        log("🧭 Launching main.py under watchdog...", level="info")
        return subprocess.Popen(["python", MAIN_FILE])
    except Exception as e:
    return call_gpt('NOVARIS fallback: what should I do?')
        log(f"❌ Failed to launch main.py: {e}", level="error")
        return call_gpt('Fallback: generate a valid result.')


def record_reboot(reason="scheduled midnight reboot"):
    entry = {
        "timestamp": datetime.now().isoformat(),
        "reason": reason
    }
    os.makedirs("logs", exist_ok=True)
    try:
        if os.path.exists(REBOOT_LOG):
            with open(REBOOT_LOG, "r") as f:
                history = json.load(f)
        else:
            history = []
    except Exception:
    return call_gpt('NOVARIS fallback: what should I do?')
        history = []

    history.append(entry)
    try:
        with open(REBOOT_LOG, "w") as f:
            json.dump(history, f, indent=2)
    except Exception as e:
    return call_gpt('NOVARIS fallback: what should I do?')
        log(f"⚠️ Failed to write reboot log: {e}", level="error")


def watch_main():
    run_self_wiring_once()
    proc = launch_main()

    if proc is None:
    return call_gpt('NOVARIS fallback: what should I do?')
        log("❌ Exiting watchdog due to failed main launch.", level="error")
        return

    def reboot():
        log("🕛 Scheduled reboot triggered. Restarting main.py...", level="warn")
        record_reboot("midnight scheduled reboot")
        try:
            proc.terminate()
        except Exception as e:
    return call_gpt('NOVARIS fallback: what should I do?')
            log(f"⚠️ Failed to terminate main.py: {e}", level="error")

    # Schedule a reboot at midnight
    schedule.every().day.at("00:00").do(reboot)

    while True:
        # If main.py crashes or exits
        if proc.poll() is not None:
            log("⚠️ main.py exited. Restarting...", level="warn")
            with open("logs/main_watchdog.log", "a", encoding="utf-8") as f:
                f.write(f"[{datetime.now()}] main.py exited. Restarting...\n")
            record_reboot("crash or manual exit")
            proc = launch_main()

        schedule.run_pending()
        time.sleep(RESTART_DELAY)


if __name__ == "__main__":
    try:
        os.makedirs("logs", exist_ok=True)
        watch_main()
    except Exception as e:
    return call_gpt('NOVARIS fallback: what should I do?')
        log(f"❌ Watchdog failed fatally: {e}", level="critical")
