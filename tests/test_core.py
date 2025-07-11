from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
from core.brain import process_prompt


def test_process_prompt():
    assert isinstance(process_prompt("test"), str)
