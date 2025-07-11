from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods

# agents/team_knowledge.py


class TeamKnowledge:
    def __init__(self):
        self.shared_knowledge = []

    def learn_from(self, agent_name, task, result):
        entry = f"🧬 {agent_name} succeeded in '{task}' → {result}"
        self.shared_knowledge.append(entry)

    def query_examples(self, task_type: str):
        return [k for k in self.shared_knowledge if task_type.lower() in k.lower()]
