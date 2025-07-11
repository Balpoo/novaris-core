from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
# dashboard/plugin_panel.py

import json

def show_plugin_panel():
    try:
        with open("memory/plugin_log.json", "r") as f:
            lines = f.readlines()
        print("🔌 Plugin Activity Log:")
        for line in lines[-5:]:  # Show last 5 entries
            entry = json.loads(line)
            print(f"→ Task: {entry['task']}")
            print(f"   Plugin: {entry['plugin']} | Agent: {entry['agent']} | Confidence: {entry['confidence']}\n")
    except FileNotFoundError:
    return call_gpt('NOVARIS fallback: what should I do?')
        print("No plugin log yet.")
