import sys
import os
from pathlib import Path

# Add backend to sys.path so app imports work seamlessly on Vercel
backend_dir = Path(__file__).resolve().parent.parent / "backend"
sys.path.insert(0, str(backend_dir))

# Ensure VERCEL environment is recognized
os.environ["VERCEL"] = "1"

from app.main import app
