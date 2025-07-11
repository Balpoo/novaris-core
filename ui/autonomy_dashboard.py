from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods

# ui/autonomy_dashboard.py

from utils.autonomy_log import load_history


def show_autonomy_dashboard(limit=10):
    history = load_history()
    print(f"\n🧠 NOVARIS Autonomy History (last {limit})\n" + "-" * 50)
    for entry in history[:limit]:
        print(f"🕓 {entry['timestamp']}")
        print(f"📌 Task: {entry['task']}")
        print(
            f"🔍 Confidence: {entry['confidence']} | Risk: {entry['risk']} | Relevance: {entry['relevance']}"
        )
        print(f"🎯 Status: {entry['status']}")
        print(f"📦 Result: {entry['result']}\n")
