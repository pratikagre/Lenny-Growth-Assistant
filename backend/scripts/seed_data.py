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
            logger.info("Transcript database is empty. Seeding landmark podcast episodes...")
            seed_json_path = Path(__file__).parent.parent / "app" / "rag" / "seed_chunks.json"
            if seed_json_path.exists():
                logger.info(f"Loading pre-indexed chunks from {seed_json_path}...")
                import json
                with open(seed_json_path, "r", encoding="utf-8") as f:
                    chunks_data = json.load(f)
                for item in chunks_data:
                    chunk_obj = TranscriptChunk(
                        id=item["id"],
                        episode_slug=item["episode_slug"],
                        episode_title=item["episode_title"],
                        guest_name=item["guest_name"],
                        publish_date=item.get("publish_date"),
                        youtube_url=item.get("youtube_url"),
                        timestamp_ref=item.get("timestamp_ref"),
                        chunk_index=item["chunk_index"],
                        chunk_text=item["chunk_text"],
                        embedding_json=item["embedding_json"]
                    )
                    session.add(chunk_obj)
                await session.commit()
                logger.info(f"Successfully loaded {len(chunks_data)} chunks from pre-indexed seed.")
            else:
                # Ingest top 10 landmark episodes from raw files
                await run_ingest(limit=10)
        else:
            logger.info(f"Database already populated with {count} transcript chunks.")

if __name__ == "__main__":
    import asyncio
    asyncio.run(seed_transcripts_if_empty())
