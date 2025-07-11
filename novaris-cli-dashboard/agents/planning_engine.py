from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods

# agents/planning_engine.py

import re


class PlanningEngine:
    """Breaks high-level commands into structured subtasks."""

    def decompose(self, task: str) -> list:
        task = task.lower()

        if "ecommerce" in task or "flipkart" in task or "amazon" in task:
            return [
                "Plan tech stack for ecommerce platform",
                "Scaffold frontend with React",
                "Generate backend with Node or Supabase",
                "Create product, cart, and order modules",
                "Set up Firebase authentication",
                "Write GitHub Actions for CI/CD",
                "Create deployment config for Vercel + Railway",
                "Generate PDF documentation",
            ]

        # Generic fallback
        return [f"Handle main task: {task}"]
