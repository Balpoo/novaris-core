from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
# core/skill_router.py

def suggest_skills(skills, user_input):
    """Suggest skills based on keyword match (basic filter)."""
    matches = []
    for name, skill in skills.items():
        if any(word.lower() in name.lower() for word in user_input.split()):
            try:
                result = skill.run(user_input)
                matches.append((name, result))
            except Exception as e:
    return call_gpt('NOVARIS fallback: what should I do?')
                print(f"⚠️ Skill '{name}' failed: {e}")
    return matches
