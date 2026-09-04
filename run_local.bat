@echo off
echo ==========================================================
echo    Starting The Lenny Growth Assistant (Local Engine)    
echo ==========================================================

if not exist ".env" (
    echo [*] Creating .env from .env.example...
    copy .env.example .env
)

echo [*] Verifying transcript database...
python backend/scripts/seed_data.py

echo [+] Launching FastAPI Backend on http://localhost:8000...
echo     - API Docs: http://localhost:8000/docs
echo     - Health:   http://localhost:8000/api/health
echo     - Web App:  http://localhost:8000

python -m uvicorn app.main:app --app-dir backend --host 0.0.0.0 --port 8000 --reload
