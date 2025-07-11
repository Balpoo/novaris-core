from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
import os
import importlib.util


def load_skills(skills_folder="skills"):
    skills = {}
    for filename in os.listdir(skills_folder):
        if filename.endswith(".py") and not filename.startswith("__"):
            skill_name = filename[:-3]
            module_path = os.path.join(skills_folder, filename)
            spec = importlib.util.spec_from_file_location(skill_name, module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            skills[skill_name] = module
    return skills
