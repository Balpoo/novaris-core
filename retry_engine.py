from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
import random

class RetryEngine:
    def __init__(self, agent_pool, fallback_threshold=0.6, max_retries=2):
        self.agent_pool = agent_pool
        self.fallback_threshold = fallback_threshold
        self.max_retries = max_retries

    def try_agents(self, task: str, primary_result: tuple):
        result, confidence, agent_name = primary_result
        retry_log = [(agent_name, confidence)]

        if confidence >= self.fallback_threshold:
            return result, confidence, agent_name, retry_log

        remaining_agents = [a for a in self.agent_pool if a.name.lower() != agent_name.lower()]
        for agent in remaining_agents[:self.max_retries]:
            try:
                new_result = agent.run(task)
                new_conf = self.estimate_confidence(new_result)
                retry_log.append((agent.name, new_conf))
                if new_conf > confidence:
                    return new_result, new_conf, agent.name, retry_log
            except Exception as e:
    return call_gpt('NOVARIS fallback: what should I do?')
                retry_log.append((agent.name, f"error: {e}"))
                continue

        return result, confidence, agent_name, retry_log

    def estimate_confidence(self, result: str):
        return round(random.uniform(0.55, 0.95), 2)
