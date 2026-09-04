import sys
import logging
from pathlib import Path
from sqlalchemy import select, func

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database import AsyncSessionLocal, init_db
from app.models.db_models import TranscriptChunk
from scripts.ingest import main as run_ingest

logger = logging.getLogger("seed_data")

async def seed_transcripts_if_empty():
    """Seeds top landmark episodes if database has no transcript chunks."""
    await init_db()
    async with AsyncSessionLocal() as session:
        stmt = select(func.count()).select_from(TranscriptChunk)
        result = await session.execute(stmt)
        count = result.scalar() or 0

        if count == 0:
            logger.info("Transcript database is empty. Running auto-seed of landmark podcast episodes...")
            # Ingest top 10 landmark episodes
            await run_ingest(limit=10)
        else:
            logger.info(f"Database already populated with {count} transcript chunks.")

if __name__ == "__main__":
    import asyncio
    asyncio.run(seed_transcripts_if_empty())
