import pytest
import pytest_asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database import AsyncSessionLocal, init_db
from app.rag.retriever import TranscriptRetriever

@pytest_asyncio.fixture(autouse=True)
async def setup_database():
    await init_db()

@pytest.mark.asyncio
async def test_retrieval_grounding():
    async with AsyncSessionLocal() as session:
        retriever = TranscriptRetriever(session)
        # Query about Brian Chesky's product management strategy at Airbnb
        chunks, is_grounded = await retriever.retrieve_relevant_chunks(
            "Brian Chesky Airbnb product management and single roadmap",
            top_k=3
        )
        assert is_grounded is True
        assert len(chunks) > 0
        top_chunk = chunks[0]
        assert "brian" in top_chunk["guest"].lower() or "chesky" in top_chunk["guest"].lower() or "airbnb" in top_chunk["episode"].lower()
        assert "score" in top_chunk
        assert top_chunk["score"] > 0.25
        assert "citation" in top_chunk
        assert "Timestamp" in top_chunk["citation"]

@pytest.mark.asyncio
async def test_out_of_domain_refusal():
    async with AsyncSessionLocal() as session:
        retriever = TranscriptRetriever(session)
        # Completely out-of-domain query
        chunks, is_grounded = await retriever.retrieve_relevant_chunks(
            "How do I bake sourdough bread with yeast and flour in the oven?",
            top_k=3,
            similarity_threshold=0.50
        )
        # Should be below threshold
        assert is_grounded is False
        assert len(chunks) == 0
