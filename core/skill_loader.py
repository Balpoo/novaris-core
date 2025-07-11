from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods

# core/skill_loader.py

import os
import importlib.util
from core.skill_registry import skill_registry  # Global store for registered skills


def load_skills(skills_folder="skills"):
    # Dynamically import all .py files from skills/ folder
    for filename in os.listdir(skills_folder):
        if filename.endswith(".py") and not filename.startswith("__"):
            skill_name = filename[:-3]
            module_path = os.path.join(skills_folder, filename)
            spec = importlib.util.spec_from_file_location(skill_name, module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

    # After imports, return registered skills
    return skill_registry
