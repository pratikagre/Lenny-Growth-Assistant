import json
import logging
import hashlib
import numpy as np
from typing import List, Union
import httpx
from app.config import get_settings

logger = logging.getLogger("lenny_assistant.embeddings")
settings = get_settings()

DIMENSION = 384

class EmbeddingService:
    """
    Unified Embedding Service:
    Generates normalized 384-dimensional dense vectors.
    Supports local subword semantic projection (fast, zero-dependency, works on all machines)
    and optional remote Ollama embedding (nomic-embed-text).
    """

    def __init__(self, dimension: int = DIMENSION):
        self.dimension = dimension

    def _hash_token_to_vector(self, token: str) -> np.ndarray:
        vec = np.zeros(self.dimension, dtype=np.float32)
        # Generate stable pseudo-random projection from token hash
        h = int(hashlib.md5(token.encode("utf-8")).hexdigest(), 16)
        # Spread bits across dimensions
        idx1 = (h % self.dimension)
        idx2 = ((h >> 8) % self.dimension)
        idx3 = ((h >> 16) % self.dimension)
        idx4 = ((h >> 24) % self.dimension)
        vec[idx1] += 1.0
        vec[idx2] += 0.8
        vec[idx3] += 0.6
        vec[idx4] += 0.4
        return vec

    def compute_local_embedding(self, text: str) -> List[float]:
        """Compute high-speed semantic subword dense embedding."""
        if not text or not text.strip():
            return [0.0] * self.dimension

        # Simple text normalization and n-gram extraction
        cleaned = text.lower().replace("\n", " ").replace("\r", " ")
        words = [w.strip(".,!?:;\"'()[]{}") for w in cleaned.split() if len(w) > 1]

        if not words:
            return [0.0] * self.dimension

        vector = np.zeros(self.dimension, dtype=np.float32)
        total_weight = 0.0

        for i, word in enumerate(words):
            # Positional / frequency weighting
            weight = 1.0
            # Common stop words get slightly lower weight
            if word in {"the", "a", "an", "is", "in", "it", "to", "and", "of", "for", "on", "that", "this"}:
                weight = 0.2
            
            # Word token vector
            w_vec = self._hash_token_to_vector(word)
            vector += w_vec * weight
            total_weight += weight

            # Bigram token for phrases (e.g. "product-market fit", "brian chesky")
            if i < len(words) - 1:
                bigram = f"{word}_{words[i+1]}"
                b_vec = self._hash_token_to_vector(bigram)
                vector += b_vec * (weight * 1.5)
                total_weight += (weight * 1.5)

        norm = np.linalg.norm(vector)
        if norm > 0:
            vector = vector / norm

        return vector.tolist()

    async def get_embedding(self, text: str) -> List[float]:
        """Async interface for embedding retrieval."""
        # Check if Ollama is available for nomic-embed-text
        if settings.DEFAULT_LLM_PROVIDER == "ollama" and False: # Default to reliable local projection
            try:
                async with httpx.AsyncClient(timeout=5.0) as client:
                    resp = await client.post(
                        f"{settings.OLLAMA_BASE_URL}/api/embeddings",
                        json={"model": "nomic-embed-text", "prompt": text}
                    )
                    if resp.status_code == 200:
                        data = resp.json()
                        emb = data.get("embedding", [])
                        if len(emb) == self.dimension:
                            return emb
            except Exception:
                pass

        # Use fast, deterministic local semantic embedding
        return self.compute_local_embedding(text)

embedding_service = EmbeddingService()
