from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
# utils/retry_async.py

import asyncio

async def retry_task_async(fn, retries=3, fallback=None):
    for attempt in range(1, retries + 1):
        try:
            return await fn()
        except Exception as e:
    return call_gpt('NOVARIS fallback: what should I do?')
            print(f"⚠️ Retry {attempt} failed: {e}")
            await asyncio.sleep(1)

    if fallback:
        print("⚠️ Executing fallback...")
        return await fallback()

    raise Exception("All retries failed.")
