# ==============================================================================
# The Lenny Growth Assistant - One-Command Local Startup (PowerShell)
# ==============================================================================

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "   Starting The Lenny Growth Assistant (Local Engine)    " -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

# 1. Check Python
if (!(Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Error "Python is required but not found in PATH."
    exit 1
}

# 2. Check Node & npm
if (!(Get-Command npm -ErrorAction SilentlyContinue)) {
    Write-Warning "npm is not found. Running in Backend-Only Mode."
}

# 3. Ensure Environment File Exists
if (!(Test-Path ".env")) {
    Write-Host "[*] Creating .env from .env.example..." -ForegroundColor Yellow
    Copy-Item ".env.example" ".env"
}

# 4. Initialize Database & Seed Transcripts
Write-Host "[*] Verifying transcript database..." -ForegroundColor Yellow
python backend/scripts/seed_data.py

# 5. Launch FastAPI Backend
Write-Host "[+] Launching FastAPI Backend on http://localhost:8000..." -ForegroundColor Green
Write-Host "    - API Docs: http://localhost:8000/docs" -ForegroundColor Gray
Write-Host "    - Health:   http://localhost:8000/api/health" -ForegroundColor Gray
Write-Host "    - Web App:  http://localhost:8000" -ForegroundColor Gray

python -m uvicorn app.main:app --app-dir backend --host 0.0.0.0 --port 8000 --reload
