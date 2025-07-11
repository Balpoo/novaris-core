from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
from agents.content_agent import ContentAgent
from agents.code_agent import CodeAgent
from agents.research_agent import ResearchAgent
from agents.planning_agent import PlanningAgent
from agents.web_agent import WebAgent
from memory.embedding_store import EmbeddingStore
import random


class AdaptiveAgent:
    def __init__(self):
        self.content_agent = ContentAgent()
        self.code_agent = CodeAgent()
        self.research_agent = ResearchAgent()
        self.planning_agent = PlanningAgent()
        self.web_agent = WebAgent()
        self.memory_store = EmbeddingStore()
        self.fallback_threshold = 0.6

    def handle_task(self, task: str, injected_hint=None):
        original_task = task
        agent_type = self.classify_task(task)

        if injected_hint:
            task += f"\n\n[Web Hint]: {injected_hint}"

        context_list = self.retrieve_context(task)
        if context_list:
            context_text = "\n".join(context_list)
            print(f"\n🧠 Retrieved Context:\n- " + "\n- ".join(context_list) + "\n")
            task += f"\n\n[Related Memory Context]:\n{context_text}"

        primary_agent = self.route_agent(agent_type)
        result = primary_agent.run(task)
        confidence = self.estimate_confidence(result)

        self.store_result(original_task, result)
        return result, confidence, agent_type

    def route_agent(self, agent_type):
        return {
            "content": self.content_agent,
            "code": self.code_agent,
            "research": self.research_agent,
            "planning": self.planning_agent,
            "web": self.web_agent,
        }.get(agent_type, self.content_agent)

    def classify_task(self, task: str):
        task = task.lower()
        if any(x in task for x in ["bug", "fix", "error", ".py", "code", "auth"]):
            return "code"
        elif any(x in task for x in ["plan", "calendar", "schedule"]):
            return "planning"
        elif any(x in task for x in ["trend", "research", "find", "latest"]):
            return "research"
        elif any(x in task for x in ["write", "quote", "story", "script", "caption"]):
            return "content"
        else:
            return "content"

    def estimate_confidence(self, result: str):
        return round(random.uniform(0.55, 0.95), 2)

    def retrieve_context(self, task: str):
        results = self.memory_store.query(task, n_results=3)
        return results.get("documents", [[]])[0]

    def store_result(self, task: str, result: str):
        self.memory_store.add(text=result, metadata={"task": task})
