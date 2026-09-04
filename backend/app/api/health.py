import time
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.database import get_db_session
from app.providers.ollama_provider import OllamaProvider
from app.providers.cloud_provider import CloudProvider
from app.models.schemas import HealthResponse

router = APIRouter(prefix="/api/health", tags=["Health & Diagnostics"])

@router.get("", response_model=HealthResponse)
async def health_check(session: AsyncSession = Depends(get_db_session)):
    """
    Comprehensive operational health endpoint:
    Probes DB latency, Ollama model availability, Cloud keys, and Vector index state.
    """
    # 1. Database Probe
    db_health = {"status": "unknown"}
    start_db = time.time()
    try:
        await session.execute(text("SELECT 1;"))
        db_health = {
            "status": "connected",
            "latency_ms": round((time.time() - start_db) * 1000, 2)
        }
    except Exception as e:
        db_health = {
            "status": "error",
            "error": str(e)
        }

    # 2. Vector Index Count Probe
    vector_health = {"status": "unknown", "chunks_indexed": 0}
    try:
        result = await session.execute(text("SELECT count(*) FROM transcript_chunks;"))
        count = result.scalar() or 0
        vector_health = {
            "status": "ready" if count > 0 else "empty",
            "chunks_indexed": count
        }
    except Exception as e:
        vector_health = {
            "status": "error",
            "error": str(e)
        }

    # 3. Ollama Probe
    ollama_provider = OllamaProvider()
    ollama_health = await ollama_provider.check_health()

    # 4. Cloud Providers Probe
    cloud_provider = CloudProvider()
    cloud_health = await cloud_provider.check_health()

    overall_status = "healthy" if db_health.get("status") == "connected" else "degraded"

    return HealthResponse(
        status=overall_status,
        database=db_health,
        ollama=ollama_health,
        cloud_providers=cloud_health,
        vector_index=vector_health,
        version="1.0.0"
    )
