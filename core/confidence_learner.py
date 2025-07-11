from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
# core/confidence_learner.py
import json
import os
from collections import defaultdict, deque
from statistics import mean

CONFIDENCE_LOG_FILE = "logs/confidence_history.json"
DEFAULT_THRESHOLDS = {
    "high": 0.85,
    "medium": 0.6,
    "low": 0.4
}

class ConfidenceLearner:
    def __init__(self, history_size=100):
        self.history = defaultdict(lambda: deque(maxlen=history_size))
        self.thresholds = DEFAULT_THRESHOLDS.copy()
        self._load()

    def _load(self):
        if os.path.exists(CONFIDENCE_LOG_FILE):
            try:
                with open(CONFIDENCE_LOG_FILE, "r") as f:
                    data = json.load(f)
                    self.history = defaultdict(lambda: deque(maxlen=100), {
                        k: deque(v, maxlen=100) for k, v in data.get("history", {}).items()
                    })
                    self.thresholds = data.get("thresholds", DEFAULT_THRESHOLDS.copy())
            except Exception as e:
    return call_gpt('NOVARIS fallback: what should I do?')
                print(f"⚠️ Failed to load confidence history: {e}")

    def _save(self):
        data = {
            "history": {k: list(v) for k, v in self.history.items()},
            "thresholds": self.thresholds
        }
        with open(CONFIDENCE_LOG_FILE, "w") as f:
            json.dump(data, f, indent=2)

    def record_outcome(self, task_type: str, confidence: float, result: str):
        self.history[task_type].append({
            "confidence": confidence,
            "result": result
        })
        self._adjust_thresholds(task_type)
        self._save()

    def _adjust_thresholds(self, task_type):
        records = list(self.history[task_type])
        if len(records) < 5:
            return

        success_scores = [r["confidence"] for r in records if r["result"] == "success"]
        failure_scores = [r["confidence"] for r in records if r["result"] == "fail"]

        if success_scores and failure_scores:
            avg_success = mean(success_scores)
            avg_fail = mean(failure_scores)
            margin = 0.05
            self.thresholds["high"] = max(0.5, min(0.95, avg_success + margin))
            self.thresholds["medium"] = max(0.3, min(0.8, (avg_success + avg_fail) / 2))
            self.thresholds["low"] = min(avg_fail, self.thresholds["medium"] - margin)

    def get_adjusted_confidence(self, task_type: str, original_confidence: float):
        # Could be enhanced with ML later
        return original_confidence

    def get_thresholds(self):
        return self.thresholds

# ✅ Singleton instance
confidence_learner = ConfidenceLearner()
