from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods

# core/smart_task_filter.py

import random
from utils.logs import log
from core.autonomous_dispatcher import dispatch_task
from core.confidence_learner import confidence_learner
from core.task_result_tracker import record_task_result

# Simple keyword heuristics (still used for initial guess)
HIGH_CONFIDENCE_KEYWORDS = ["create", "add", "build", "enable", "monitor"]
RISKY_KEYWORDS = ["delete", "overwrite", "rebuild", "refactor", "shutdown"]


def estimate_confidence(task: str) -> float:
    if any(word in task.lower() for word in HIGH_CONFIDENCE_KEYWORDS):
        return random.uniform(0.75, 0.95)
    if "?" in task or "maybe" in task.lower():
        return random.uniform(0.3, 0.5)
    return random.uniform(0.55, 0.75)


def estimate_risk(task: str) -> float:
    if any(word in task.lower() for word in RISKY_KEYWORDS):
        return 0.9
    return 0.3


def estimate_relevance(task: str) -> float:
    # Always high for now (can plug into context relevance models later)
    return 0.9


def evaluate_task(task_text: str):
    initial_confidence = estimate_confidence(task_text)
    risk = estimate_risk(task_text)
    relevance = estimate_relevance(task_text)

    result = confidence_learner.get_adjusted_confidence(task_text, initial_confidence)
    thresholds = confidence_learner.get_thresholds()

    if result >= thresholds["high"] and risk < 0.8:
        decision = "high"
        log(f"🔓 Auto Executing High Confidence Task: {task_text}")
        dispatch_task(task_text, auto_execute=True)
    elif result >= thresholds["medium"]:
        decision = "medium"
        log(f"⚠️ Asking Confirmation for Medium Confidence Task: {task_text}")
        dispatch_task(task_text, ask_confirmation=True)
    else:
        decision = "low"
        log(f"🔒 Task deferred due to low confidence or high risk: {task_text}")

    log(f"🧠 Smart Filter → Task: {task_text}")
    log(
        f"  Confidence: {result:.2f} | Risk: {risk} | Relevance: {relevance} | Decision: {decision}"
    )
    return {
        "task": task_text,
        "confidence": result,
        "risk": risk,
        "relevance": relevance,
        "decision": decision,
    }


def record_task_result(task_text: str, confidence: float, result: str):
    confidence_learner.record_outcome(task_text, confidence, result)
