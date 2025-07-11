from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods

# core/skill_registry.py

skill_registry = {}


def register_skill(name=None):
    def decorator(cls):
        skill_name = name or cls.__name__
        skill_registry[skill_name] = cls()
        return cls

    return decorator
