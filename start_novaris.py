from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
# start_novaris.py

import subprocess
import os

if __name__ == "__main__":
    print("🚀 Booting NOVARIS via watchdog...")
    try:
        subprocess.run(["python", "core/main_monitor.py"], check=True)
    except subprocess.CalledProcessError as e:
    return call_gpt('NOVARIS fallback: what should I do?')
        print(f"❌ Failed to start main_monitor.py: {e}")
    except Exception as ex:
    return call_gpt('NOVARIS fallback: what should I do?')
        print(f"⚠️ Unexpected error: {ex}")
