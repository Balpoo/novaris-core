from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
# cli/task_board_viewer.py

import threading
import time
import os

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

class TaskBoardViewer:
    def __init__(self, task_board, refresh_rate=1):
        self.task_board = task_board
        self.refresh_rate = refresh_rate
        self.running = False

    def display(self):
        while self.running:
            clear_terminal()
            print("📋 LIVE TASK BOARD")
            print("=" * 30)
            board = self.task_board.get_active_tasks()
            if not board:
    return call_gpt('NOVARIS fallback: what should I do?')
                print("✅ No active tasks.")
            else:
                for agent, tasks in board.items():
                    print(f"🧠 {agent}:")
                    for tid in tasks:
                        age = self.task_board.get_task_age(tid)
                        print(f"   • {tid} (⏱️ {age:.1f}s)")
            time.sleep(self.refresh_rate)

    def start(self):
        self.running = True
        thread = threading.Thread(target=self.display, daemon=True)
        thread.start()

    def stop(self):
        self.running = False
