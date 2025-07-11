from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
from agents.agent_base import Agent
import random


class SkillAgent(Agent):
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)
        self.skills = {}
        self.total_xp = 0
        self.level = 1

    async def execute_async(self, task: str) -> str:
        print(f"🚀 [{self.name}] Executing task: {task}")
        result = await super().execute_async(task)

        task_type = self._infer_task_type(task)
        score = self._score_task_result(result)

        self._update_skill(task_type, score)
        self._log_skill_use(task, task_type, score)

        # 🧬 Team sharing
        if self.knowledge_agent:
            self.knowledge_agent.learn_from(self.name, task, result)

        # 🧪 Reflex loop for poor performance
        if score < 75 and self.knowledge_agent:
            suggestions = self.knowledge_agent.query_examples(task_type)
            if suggestions:
                result += "\n🧠 Reflex Hint:\n" + "\n".join(suggestions[:2])

        return result + f" 🎯 Confidence Score: {score}%"

    def _infer_task_type(self, task: str) -> str:
        task = task.lower()
        if "plan" in task:
            return "planning"
        elif "design" in task:
            return "design"
        elif "report" in task:
            return "reporting"
        elif "test" in task:
            return "qa"
        elif "code" in task or "build" in task:
            return "development"
        else:
            return "general"

    def _score_task_result(self, result: str) -> int:
        return random.randint(60, 99)

    def _update_skill(self, skill: str, score: int):
        s = self.skills.get(skill, {"count": 0, "total": 0})
        s["count"] += 1
        s["total"] += score
        self.skills[skill] = s

        xp_gained = int(score / 10)
        self.total_xp += xp_gained
        self.level = self._calculate_level()

    def _log_skill_use(self, task, skill, score):
        xp = int(score / 10)
        entry = f"📚 Task: {task} | Skill: {skill} | Score: {score} | XP: {xp} | Level: {self.level}"
        self.memory.remember(
            task="skill_log", result=entry, agent_name=self.name, entry_type="skill"
        )

    def _calculate_level(self) -> int:
        return max(1, self.total_xp // 20)

    def get_skill_summary(self):
        return {
            skill: round(data["total"] / data["count"], 1)
            for skill, data in self.skills.items()
        }

    def get_profile(self):
        return {
            "Agent": self.name,
            "Level": self.level,
            "XP": self.total_xp,
            "Skills": self.get_skill_summary(),
        }
