import json
import logging
import numpy as np
from typing import List, Dict, Any, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, text
from app.models.db_models import TranscriptChunk
from app.rag.embeddings import embedding_service
from app.config import get_settings

logger = logging.getLogger("lenny_assistant.retriever")
settings = get_settings()

class TranscriptRetriever:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def retrieve_relevant_chunks(
        self,
        query: str,
        top_k: int = None,
        similarity_threshold: float = None
    ) -> Tuple[List[Dict[str, Any]], bool]:
        """
        Retrieves top-k relevant transcript chunks matching the query.
        Returns: (chunks_list, is_grounded_bool)
        If no chunks pass the threshold, is_grounded_bool is False.
        """
        top_k = top_k or settings.RAG_TOP_K
        threshold = similarity_threshold if similarity_threshold is not None else settings.RAG_SIMILARITY_THRESHOLD

        # 1. Compute query embedding
        query_vector = await embedding_service.get_embedding(query)
        q_np = np.array(query_vector, dtype=np.float32)
        q_norm = np.linalg.norm(q_np)
        if q_norm > 0:
            q_np = q_np / q_norm

        # 2. Fetch all transcript chunks from DB
        # For our local / embedded corpus (~15-50 seeded key episodes or full collection)
        stmt = select(TranscriptChunk)
        result = await self.session.execute(stmt)
        chunks = result.scalars().all()

        if not chunks:
            logger.warning("No transcript chunks present in database. Please run ingestion script.")
            return [], False

        scored_chunks = []
        for chunk in chunks:
            try:
                emb = json.loads(chunk.embedding_json)
                c_np = np.array(emb, dtype=np.float32)
                c_norm = np.linalg.norm(c_np)
                if c_norm > 0:
                    c_np = c_np / c_norm
                
                # Cosine similarity is dot product of normalized vectors
                sim = float(np.dot(q_np, c_np))
                
                # Bonus match if query explicitly names the guest (e.g. "Brian Chesky")
                query_lower = query.lower()
                if chunk.guest_name and chunk.guest_name.lower() in query_lower:
                    sim = min(1.0, sim + 0.25)
                
                scored_chunks.append((sim, chunk))
            except Exception as e:
                logger.error(f"Error computing similarity for chunk {chunk.id}: {e}")
                continue

        # Sort descending by similarity score
        scored_chunks.sort(key=lambda x: x[0], reverse=True)
        top_matches = scored_chunks[:top_k]

        # Check if top score meets the threshold
        top_score = top_matches[0][0] if top_matches else 0.0
        logger.info(f"Top retrieval similarity for '{query[:40]}...': {top_score:.4f} (Threshold: {threshold})")

        if top_score < threshold:
            logger.info("Top retrieval score is below threshold. Refusal protocol indicated.")
            return [], False

        formatted_results = []
        for sim, chunk in top_matches:
            formatted_results.append({
                "id": chunk.id,
                "episode": chunk.episode_title,
                "guest": chunk.guest_name,
                "timestamp": chunk.timestamp_ref or "00:00:00",
                "publish_date": chunk.publish_date,
                "youtube_url": chunk.youtube_url,
                "text": chunk.chunk_text,
                "score": round(sim, 4),
                "citation": f"[Episode: {chunk.episode_title}, Guest: {chunk.guest_name}, Timestamp: {chunk.timestamp_ref or '00:00:00'}]"
            })

        return formatted_results, True
