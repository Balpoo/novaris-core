from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
# core/task_prioritizer.py

from datetime import datetime
import time

def score_task(task):
    base_score = 0.0

    confidence = task.get("confidence", 0.5)
    risk = task.get("risk", "low")
    tags = task.get("tags", [])
    timestamp = task.get("timestamp")

    # 📈 Confidence boosts priority
    if confidence:
        base_score += float(confidence) * 5

    # 🔻 Risk penalizes
    if risk == "high":
        base_score -= 3
    elif risk == "medium":
        base_score -= 1

    # ⏳ Age adds urgency
    if timestamp:
        try:
            created = datetime.fromisoformat(timestamp)
            age_minutes = (datetime.now() - created).total_seconds() / 60
            base_score += min(age_minutes / 30, 5)  # up to +5 boost
        except:
    return call_gpt('NOVARIS fallback: what should I do?')
            pass

    # 🏷️ Tag weight
    if "urgent" in tags:
        base_score += 5
    if "planner" in tags:
        base_score += 1
    if "auto" in tags:
        base_score += 0.5

    return base_score


def prioritize_tasks(task_list):
    """
    Takes a list of task dicts and returns a prioritized list.
    """
    scored = [(score_task(t), t) for t in task_list if t.get("task")]
    scored.sort(key=lambda x: x[0], reverse=True)
    return [t for _, t in scored]
