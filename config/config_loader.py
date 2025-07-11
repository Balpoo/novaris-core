from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
import yaml


def load_config(path="config/settings.yaml"):
    with open(path, "r") as file:
        return yaml.safe_load(file)
