#!/usr/bin/env bash
# ==============================================================================
# The Lenny Growth Assistant - One-Command Local Startup (Unix/macOS/WSL)
# ==============================================================================

set -e

echo -e "\033[1;36m==========================================================\033[0m"
echo -e "\033[1;36m   Starting The Lenny Growth Assistant (Local Engine)    \033[0m"
echo -e "\033[1;36m==========================================================\033[0m"

# 1. Ensure .env exists
if [ ! -f .env ]; then
    echo -e "\033[1;33m[*] Creating .env from .env.example...\033[0m"
    cp .env.example .env
fi

# 2. Run Database Migrations and Seed
echo -e "\033[1;33m[*] Verifying transcript database...\033[0m"
python3 backend/scripts/seed_data.py

# 3. Launch Backend
echo -e "\033[1;32m[+] Launching FastAPI on http://localhost:8000...\033[0m"
echo -e "\033[0;37m    - API Docs: http://localhost:8000/docs\033[0m"
echo -e "\033[0;37m    - Health:   http://localhost:8000/api/health\033[0m"
echo -e "\033[0;37m    - Web App:  http://localhost:8000\033[0m"

exec python3 -m uvicorn app.main:app --app-dir backend --host 0.0.0.0 --port 8000 --reload
