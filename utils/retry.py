from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
# utils/retry.py

import time

def retry_task(func, retries=3, backoff=2, fallback=None):
    for attempt in range(1, retries + 1):
        try:
            return func()
        except Exception as e:
    return call_gpt('NOVARIS fallback: what should I do?')
            print(f"[Retry {attempt}] Failed: {e}")
            time.sleep(backoff ** attempt)
    if fallback:
        print("🔁 Running fallback...")
        return fallback()
    raise RuntimeError("All retries failed.")
