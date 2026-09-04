import logging
from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.database import init_db
from app.api import health_router, sessions_router, chat_router

# Configure Structured Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("lenny_assistant")
settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up The Lenny Growth Assistant API...")
    # Initialize DB tables
    await init_db()
    
    # Auto-seed core transcripts if DB is empty
    try:
        from scripts.seed_data import seed_transcripts_if_empty
        await seed_transcripts_if_empty()
    except Exception as e:
        logger.warning(f"Auto-seeding check completed with notice: {e}")
        
    logger.info("Application startup complete.")
    yield
    logger.info("Shutting down The Lenny Growth Assistant API...")

app = FastAPI(
    title="The Lenny Growth Assistant API",
    description="Enterprise-grade RAG and Content Engine for Lenny's Podcast Transcripts",
    version="1.0.0",
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list + ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global Exception Handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled error processing {request.method} {request.url.path}: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "An unexpected error occurred processing your request.",
                "detail": str(exc)
            }
        }
    )

# Include Routers
app.include_router(health_router)
app.include_router(sessions_router)
app.include_router(chat_router)

@app.get("/api/info")
async def api_info():
    return {
        "name": "The Lenny Growth Assistant API",
        "status": "online",
        "version": "1.0.0",
        "docs_url": "/docs",
        "health_url": "/api/health"
    }

# Mount Frontend static build if available
dist_path = Path(__file__).parent.parent.parent / "frontend" / "dist"
if dist_path.exists():
    logger.info(f"Mounting frontend static bundle from {dist_path}")
    assets_dir = dist_path / "assets"
    if assets_dir.exists():
        app.mount("/assets", StaticFiles(directory=str(assets_dir)), name="assets")

    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        if full_path.startswith("api/") or full_path == "api" or full_path.startswith("docs") or full_path.startswith("openapi.json"):
            return JSONResponse(status_code=404, content={"error": "Endpoint Not Found"})
        target_file = dist_path / full_path
        if target_file.exists() and target_file.is_file():
            return FileResponse(target_file)
        return FileResponse(dist_path / "index.html")
else:
    @app.get("/")
    async def root():
        return {
            "name": "The Lenny Growth Assistant API",
            "status": "online",
            "version": "1.0.0",
            "docs_url": "/docs",
            "health_url": "/api/health",
            "notice": "Frontend bundle not yet built. Run 'npm run build' in frontend directory."
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, reload=True)
