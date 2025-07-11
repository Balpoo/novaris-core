from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods

# core/trust_manager.py


class TrustManager:
    def __init__(self):
        # Default trust scores per agent and task type
        self.trust_scores = {"executor": {"file_cleanup": 0.95, "data_migration": 0.80}}

    def get_trust_score(self, agent: str, task_type: str) -> float:
        return self.trust_scores.get(agent, {}).get(task_type, 0.5)

    def update_trust_score(self, agent: str, task_type: str, success: bool):
        current = self.get_trust_score(agent, task_type)
        delta = 0.05 if success else -0.1
        new_score = max(0.0, min(1.0, current + delta))
        self.trust_scores.setdefault(agent, {})[task_type] = new_score
