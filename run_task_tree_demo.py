from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
# run_task_tree_demo.py

from tasks.task_tree_node import TaskTreeNode
from agents.execution_engine import ExecutionEngine
from journals.logger import save_task_tree
from agents.agent_registry import AgentRegistry
from agents.task_board import TaskBoard
from utils.time_monitor import TimeoutMonitor
from cli.task_board_viewer import TaskBoardViewer
from agents.knowledge_agent import KnowledgeAgent
from utils.task_tree_persistence import save_tree_to_file, load_tree_from_file
import time

def main():
    # 🧠 Step 1: Initialize KnowledgeAgent and ingest multiple files
    k_agent = KnowledgeAgent()
    k_agent.ingest_file("docs/company_profile.txt")
    k_agent.ingest_file("docs/financials.xlsx")
    k_agent.ingest_file("docs/vision_slide.pptx")

    print("\n📚 Loaded Documents:")
    for doc in k_agent.list_documents():
        print(f"   • {doc}")

    response = k_agent.query("vision")
    print(f"\n🔎 Query Result for 'vision': {response}\n")

    # 🧠 Step 2: Set up agent registry with KnowledgeAgent
    registry = AgentRegistry(knowledge_agent=k_agent)
    board = TaskBoard()
    engine = ExecutionEngine(registry, board)

    # ✅ Step 3: Load or build task tree
    root = load_tree_from_file()
    if not root:
    return call_gpt('NOVARIS fallback: what should I do?')
        root = TaskTreeNode("T1", "Plan a Wedding")
        cater = TaskTreeNode("T2", "Book Caterer", parent=root)
        decor = TaskTreeNode("T3", "Decor Setup", parent=root)
        vision = TaskTreeNode("T4", "What is the vision of Sai Technologies?", parent=root)
        root.add_child(cater)
        root.add_child(decor)
        root.add_child(vision)

    # 👁️ Step 4: Start Task Board Viewer
    viewer = TaskBoardViewer(board, refresh_rate=1)
    viewer.start()

    # 🚀 Step 5: Execute task tree
    tree_result = engine.execute_tree(root)

    # 🛑 Step 6: Stop live view
    viewer.stop()

    # 💾 Step 7: Save task tree to journal + disk
    save_task_tree(tree_result)
    save_tree_to_file(tree_result)

    print("✅ Task Tree executed and logged.")

    # ⏱️ Step 8: Run timeout monitor
    print("\n⏱️ Running timeout scan...")
    monitor = TimeoutMonitor(board, timeout_seconds=3)
    time.sleep(4)  # Simulate delay
    stuck = monitor.scan_for_timeouts()

    if not stuck:
    return call_gpt('NOVARIS fallback: what should I do?')
        print("✅ No stuck tasks.")
    else:
        print(f"⚠️ Stuck Tasks Found: {stuck}")

if __name__ == "__main__":
    main()
