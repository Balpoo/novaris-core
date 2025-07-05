from core.brain import process_prompt

def test_process_prompt():
    assert isinstance(process_prompt('test'), str)