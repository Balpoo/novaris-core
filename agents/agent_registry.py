# core/agent_registry.py


# TEMP SAFE fallback: disable call_gpt during recovery
def call_gpt(message):
    print(f"[FAKE GPT CALLED] {message}")
    return f"[Simulated GPT Fallback] {message}"


class AgentRegistry:
    def __init__(self):
        self.registry = {}

    def register(self, name, agent):
        self.registry[name] = agent

    def get(self, name):
        return self.registry.get(name, None)

    def get_all(self):
        return self.registry

    def fallback_if_missing(self, name):
        if name not in self.registry:
            return call_gpt(
                f"[NOVARIS Fallback] Agent '{name}' not found. What should I do?"
            )
