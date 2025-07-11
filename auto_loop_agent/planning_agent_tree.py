from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods

# agents/planning_agent_tree.py


class PlanningTreeAgent:
    def generate_task_tree(self, high_level_goal: str):
        goal = high_level_goal.lower()

        if "instagram" in goal and "campaign" in goal:
            return [
                "Research trending Instagram reel formats for festive campaigns",
                "Plan content calendar for Ganesh Chaturthi (7 days)",
                "Generate 3 reels and 3 stories using brand tone",
                "Write captions and festive hashtags",
                "Schedule posts and set up reminders",
                "Monitor engagement and prepare insights report",
            ]

        elif "website launch" in goal:
            return [
                "Create launch checklist",
                "Write homepage and about us content",
                "Design banners and CTA sections",
                "Prepare email campaign for announcement",
                "Connect analytics + social tracking",
            ]

        elif "youtube" in goal and "series" in goal:
            return [
                "Define theme and episode flow",
                "Research similar successful channels",
                "Script intro + outro",
                "Design thumbnail templates",
                "Create upload schedule and checklist",
            ]

        else:
            return [
                f"Breakdown of: {high_level_goal}",
                "Step 1: Understand core objective",
                "Step 2: Research related tasks",
                "Step 3: Execute iteratively",
            ]
