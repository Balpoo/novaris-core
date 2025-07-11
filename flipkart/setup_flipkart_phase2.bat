@echo off
cd /d D:\Karan\Documents\Projects\novaris-core\flipkart

:: Make folders
mkdir agents
mkdir dashboard
mkdir config
mkdir utils
mkdir docs
mkdir scripts

:: Create run_dashboard.py
echo from dashboard.app import FlipkartDashboard > run_dashboard.py
echo. >> run_dashboard.py
echo if __name__ == "__main__": >> run_dashboard.py
echo     FlipkartDashboard().run() >> run_dashboard.py

:: Create dashboard/app.py
(
echo from agents.planning_agent import PlanningAgent
echo from agents.filing_agent import FilingAgent
echo from agents.memory_agent import MemoryAgent
echo.
echo class FlipkartDashboard:
echo     def __init__(self):
echo         self.agents = [
echo             PlanningAgent(),
echo             FilingAgent(),
echo             MemoryAgent()
echo         ]
echo.
echo     def run(self):
echo         print("🧠 NOVARIS Flipkart CLI is running.")
echo         while True:
echo             task = input("^"\nEnter a master task (or 'exit'): ^")
echo             if task.lower() == 'exit':
echo                 print("👋 Exiting...")
echo                 break
echo             handled = False
echo             for agent in self.agents:
echo                 if agent.can_handle(task):
echo                     result, confidence, agent_name = agent.handle(task)
echo                     print(f"✅ {agent_name} handled the task with confidence {confidence:.2f}")
echo                     print(f"🧩 Result: {result}")
echo                     handled = True
echo                     break
echo             if not handled:
echo                 print("⚠️ No agent could handle this task. Try rephrasing.")
) > dashboard\app.py

:: Agents
echo class PlanningAgent:^> agents\planning_agent.py
echo     def can_handle(self, task: str) -^> bool:^> >> agents\planning_agent.py
echo         return "plan" in task.lower() or "create" in task.lower() or "design" in task.lower() >> agents\planning_agent.py
echo. >> agents\planning_agent.py
echo     def handle(self, task: str): >> agents\planning_agent.py
echo         result = f"Planned step-by-step execution for: {task}" >> agents\planning_agent.py
echo         confidence = 0.92 >> agents\planning_agent.py
echo         return result, confidence, "PlanningAgent" >> agents\planning_agent.py

echo class FilingAgent:^> agents\filing_agent.py
echo     def can_handle(self, task: str) -^> bool:^> >> agents\filing_agent.py
echo         return "file" in task.lower() or "submit" in task.lower() >> agents\filing_agent.py
echo. >> agents\filing_agent.py
echo     def handle(self, task: str): >> agents\filing_agent.py
echo         result = f"Filed required documents for: {task}" >> agents\filing_agent.py
echo         confidence = 0.87 >> agents\filing_agent.py
echo         return result, confidence, "FilingAgent" >> agents\filing_agent.py

echo class MemoryAgent:^> agents\memory_agent.py
echo     def can_handle(self, task: str) -^> bool:^> >> agents\memory_agent.py
echo         return "remember" in task.lower() or "log" in task.lower() >> agents\memory_agent.py
echo. >> agents\memory_agent.py
echo     def handle(self, task: str): >> agents\memory_agent.py
echo         result = f"Memory log created for task: {task}" >> agents\memory_agent.py
echo         confidence = 0.95 >> agents\memory_agent.py
echo         return result, confidence, "MemoryAgent" >> agents\memory_agent.py

:: Config
echo AGENT_LIST = ["PlanningAgent", "FilingAgent", "MemoryAgent"] > config\agent_registry.py

:: Utils
echo def route_task(task: str) -^> str:^> > utils\task_router.py
echo     if "plan" in task:^> return "PlanningAgent" >> utils\task_router.py
echo     elif "file" in task:^> return "FilingAgent" >> utils\task_router.py
echo     return "MemoryAgent" >> utils\task_router.py

:: Docs
echo ## Agent Routing Tree > docs\AGENT_MAP.md
echo - PlanningAgent → tasks with 'plan', 'create', 'design' >> docs\AGENT_MAP.md
echo - FilingAgent → tasks with 'file', 'submit' >> docs\AGENT_MAP.md
echo - MemoryAgent → tasks with 'log', 'remember' >> docs\AGENT_MAP.md

:: README
echo # NOVARIS Flipkart Phase 2 > README.md
echo This module handles adaptive task delegation via agents. >> README.md

:: Vercel
echo { "rewrites": [{ "source": "/(.*)", "destination": "/api" }] } > vercel.json

:: Deploy script
echo @echo off > scripts\deploy.sh
echo echo Deploying Flipkart Project >> scripts\deploy.sh
echo git init >> scripts\deploy.sh
echo git add . >> scripts\deploy.sh
echo git commit -m "🚀 Phase 2: Flipkart Agents Initialized" >> scripts\deploy.sh
echo git remote add origin https://github.com/YOUR_USERNAME/flipkart-novaris.git >> scripts\deploy.sh
echo git push -u origin main >> scripts\deploy.sh
echo vercel --prod >> scripts\deploy.sh

echo ✅ Flipkart Phase 2 files generated.
pause
