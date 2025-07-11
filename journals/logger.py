from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods

# journals/logger.py

import json
from datetime import datetime


def save_task_tree(tree_dict, filename="journals/task_journal.json"):
    log_entry = {"timestamp": datetime.now().isoformat(), "task_tree": tree_dict}
    with open(filename, "a") as f:
        json.dump(log_entry, f)
        f.write("\n")
