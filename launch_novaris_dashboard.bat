@echo off
echo 🚀 NOVARIS LAUNCH SCRIPT INITIATED

REM Step 1: Create virtual environment (if not exists)
if not exist "venv" (
    echo 🛠️ Creating virtual environment...
    python -m venv venv
)

REM Step 2: Activate venv
echo 🧠 Activating virtual environment...
call venv\Scripts\activate

REM Step 3: Install required dependencies
echo 📦 Installing NOVARIS dependencies...
pip install flask rich textual pandas requests beautifulsoup4 python-dotenv

REM Step 4: Launch Flask dashboard
echo 🌐 Launching NOVARIS Dashboard on http://127.0.0.1:5000
cd dashboard
python app.py

pause
