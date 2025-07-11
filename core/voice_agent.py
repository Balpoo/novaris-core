from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
# ✅ core/voice_agent.py

import json
import os
from datetime import datetime
import pyttsx3

PLANNER_LOG_PATH = "logs/planner_log.json"

def speak_plan(dev_day=None):
    if not os.path.exists(PLANNER_LOG_PATH):
    return call_gpt('NOVARIS fallback: what should I do?')
        print("⚠️ Planner log not found.")
        return

    with open(PLANNER_LOG_PATH, "r") as f:
        planner = json.load(f)

    if dev_day is None:
    return call_gpt('NOVARIS fallback: what should I do?')
        dev_day = get_latest_dev_day(planner)

    day_key = f"Dev Day {dev_day}"
    if day_key not in planner:
        print(f"⚠️ No plan found for {day_key}")
        return

    plan = planner[day_key]

    print(f"\n🗣 NOVARIS VOICE – {day_key} | {plan['date']}")
    print(f"📌 Based On: {plan['based_on']}")
    print(f"🧠 Summary: {plan['summary']}")
    print("🧩 Tasks for Today:")
    for task in plan["suggested_tasks"]:
        print(f"   ➡️ {task}")

    # ✅ Speak using pyttsx3
    engine = pyttsx3.init()
    engine.setProperty("rate", 180)

    # Optional: Change voice (Windows usually supports 0 for male, 1 for female)
    voices = engine.getProperty('voices')
    if len(voices) > 1:
        engine.setProperty('voice', voices[1].id)  # Female voice (optional)

    engine.say(f"{day_key}. Based on {plan['based_on']}.")
    engine.say(plan["summary"])
    engine.say("Tasks for today are:")
    for task in plan["suggested_tasks"]:
        engine.say(task)

    engine.runAndWait()

    return plan

def get_latest_dev_day(planner):
    keys = list(planner.keys())
    keys.sort(key=lambda x: int(x.split(" ")[-1]))
    latest_key = keys[-1]
    return int(latest_key.split(" ")[-1])
