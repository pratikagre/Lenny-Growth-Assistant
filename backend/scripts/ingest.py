import os
import sys
import re
import json
import yaml
import asyncio
import logging
from pathlib import Path
from typing import List, Dict, Any, Tuple

# Ensure backend directory is in path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database import AsyncSessionLocal, init_db
from app.models.db_models import TranscriptChunk
from app.rag.embeddings import embedding_service
from sqlalchemy import select, delete

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("ingest")

SPEAKER_TIME_REGEX = re.compile(r'^(?:(?P<speaker>[A-Za-z\s\.\-\'\’]+)\s+)?\((?P<time>\d{2}:\d{2}:\d{2})\):\s*', re.MULTILINE)

def parse_transcript_file(file_path: Path) -> Tuple[Dict[str, Any], str]:
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    parts = content.split("---")
    if len(parts) >= 3:
        try:
            frontmatter = yaml.safe_load(parts[1]) or {}
        except Exception:
            frontmatter = {}
        body = "---".join(parts[2:]).strip()
        return frontmatter, body
    return {}, content

def chunk_transcript(body: str, max_words: int = 400, overlap_words: int = 50) -> List[Dict[str, Any]]:
    """
    Chunks transcript text into overlapping windows while preserving the nearest timestamp and speaker tag.
    """
    paragraphs = body.split("\n\n")
    chunks = []
    
    current_words = []
    current_time = "00:00:00"
    current_speaker = "Speaker"

    for p in paragraphs:
        p = p.strip()
        if not p:
            continue

        # Look for speaker timestamp header
        match = SPEAKER_TIME_REGEX.search(p)
        if match:
            if match.group("speaker"):
                current_speaker = match.group("speaker").strip()
            if match.group("time"):
                current_time = match.group("time").strip()

        words = p.split()
        current_words.extend(words)

        if len(current_words) >= max_words:
            chunk_str = " ".join(current_words)
            chunks.append({
                "text": chunk_str,
                "timestamp": current_time,
                "speaker": current_speaker
            })
            # Maintain overlap
            current_words = current_words[-overlap_words:]

    if current_words:
        chunks.append({
            "text": " ".join(current_words),
            "timestamp": current_time,
            "speaker": current_speaker
        })

    return chunks

async def ingest_episode(dir_path: Path, session) -> int:
    transcript_file = dir_path / "transcript.md"
    if not transcript_file.exists():
        return 0

    episode_slug = dir_path.name
    frontmatter, body = parse_transcript_file(transcript_file)

    guest = frontmatter.get("guest") or episode_slug.replace("-", " ").title()
    title = frontmatter.get("title") or f"Conversation with {guest}"
    pub_date = str(frontmatter.get("publish_date") or "")
    yt_url = frontmatter.get("youtube_url") or ""

    chunks = chunk_transcript(body)
    if not chunks:
        return 0

    logger.info(f"Ingesting '{title}' ({guest}) -> {len(chunks)} chunks...")

    for i, c in enumerate(chunks):
        emb = await embedding_service.get_embedding(c["text"])
        chunk_obj = TranscriptChunk(
            episode_slug=episode_slug,
            episode_title=title,
            guest_name=guest,
            publish_date=pub_date,
            youtube_url=yt_url,
            timestamp_ref=c["timestamp"],
            chunk_index=i,
            chunk_text=c["text"],
            embedding_json=json.dumps(emb)
        )
        session.add(chunk_obj)

    await session.commit()
    return len(chunks)

async def main(episodes_dir: str = None, limit: int = 15):
    await init_db()
    
    # Locate episodes directory
    candidate_paths = [
        Path(episodes_dir) if episodes_dir else None,
        Path("scratch/transcripts_sample/episodes"),
        Path("../scratch/transcripts_sample/episodes"),
        Path("episodes")
    ]
    target_dir = None
    for p in candidate_paths:
        if p and p.exists() and p.is_dir():
            target_dir = p
            break

    if not target_dir:
        logger.error("Episodes directory not found!")
        return

    logger.info(f"Found transcript archive at: {target_dir}")
    episode_folders = [f for f in target_dir.iterdir() if f.is_dir()]
    
    # Prioritize high-signal landmark episodes
    priority_slugs = [
        "brian-chesky", "elena-verna", "shreyas-doshi", "casey-winters",
        "marty-cagan", "bob-moesta", "sean-ellis", "nikita-bier",
        "guillermo-rauch", "april-dunford", "brian-balfour", "tobi-lutke"
    ]
    
    ordered_folders = []
    for slug in priority_slugs:
        folder = target_dir / slug
        if folder.exists():
            ordered_folders.append(folder)

    for f in episode_folders:
        if f not in ordered_folders:
            ordered_folders.append(f)

    if limit > 0:
        ordered_folders = ordered_folders[:limit]

    total_chunks = 0
    async with AsyncSessionLocal() as session:
        for folder in ordered_folders:
            count = await ingest_episode(folder, session)
            total_chunks += count

    logger.info(f"Successfully ingested {len(ordered_folders)} episodes ({total_chunks} total chunks).")

if __name__ == "__main__":
    limit_arg = int(sys.argv[1]) if len(sys.argv) > 1 else 15
    asyncio.run(main(limit=limit_arg))
