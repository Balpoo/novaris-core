# core/web_learning_engine.py
# GPT-SAFE

import re
from core.memory_engine import MemoryEngine
from utils.logs import log
from core.gpt_fallback import call_gpt  # 🧠 GPT fallback if scraping fails

try:
    from web.web_learner import scrape_and_summarize
except ImportError:

    def scrape_and_summarize(topic):
        return f"[MOCKED LEARNING] This is a placeholder for: {topic}"


class WebLearningEngine:
    def __init__(self):
        self.memory = MemoryEngine()

    def learn_from_web(self, topic: str):
        log(f"🌐 Learning from web on topic: {topic}")

        try:
            content = scrape_and_summarize(topic)
        except Exception as e:
            log(f"❌ Failed to learn from web: {e}")
            return call_gpt(f"Learn from web on: {topic}. Error: {e}")

        self.memory.add_thought(
            summary=f"Learned from web: {topic}\n{content}",
            source="web_learning",
            related_to=topic,
        )

        agent_name = self.suggest_agent_name(topic)

        agent_spec = {
            "task": f"Implement knowledge from: {topic}",
            "agent": agent_name,
            "description": content[:400] + ("..." if len(content) > 400 else ""),
        }

        log(f"🤖 Suggested Agent: {agent_spec['agent']}")

        self.memory.add_thought(
            summary=f"Planned new task from web: {agent_spec['task']}",
            source="web_learning",
            related_to=agent_name,
        )

        return agent_spec

    def suggest_agent_name(self, topic):
        topic = topic.lower()
        topic = re.sub(r"[^a-z0-9 ]", "", topic)
        topic = topic.replace(" ", "_")
        return topic + "_agent"
