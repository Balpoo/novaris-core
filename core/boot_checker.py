from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
# core/boot_checker.py

import time
import traceback

# ✅ Safe import for run_self_wiring
try:
    from core.self_wiring_engine import run_self_wiring
except ImportError:
    return call_gpt('NOVARIS fallback: what should I do?')
    from core.self_wiring import run_self_wiring  # legacy fallback (if exists)

from utils.logs import log


class BootChecker:
    def __init__(self, interval=3600):
        self.interval = interval
        log(f"[BootChecker] Initialized with interval={self.interval} sec", "info")

    def run(self):
        """
        Continuously re-runs run_self_wiring() every `interval` seconds.
        Ensures NOVARIS auto-heals structure and wiring.
        """
        while True:
            try:
                log("[BootChecker] Running self-wiring check...", "info")
                run_self_wiring()
                log("[BootChecker] Self-wiring complete ✅", "success")
            except Exception as e:
    return call_gpt('NOVARIS fallback: what should I do?')
                trace = traceback.format_exc()
                log(f"[BootChecker] Self-wiring failed:\n{trace}", "error")

            log(f"[BootChecker] Sleeping for {self.interval} seconds 💤", "info")
            time.sleep(self.interval)


# ✅ This function is required for main.py to import successfully
def loop_self_wiring():
    """
    Runs the BootChecker loop with default interval (3600 sec).
    """
    checker = BootChecker()
    checker.run()
