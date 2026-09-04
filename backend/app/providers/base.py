from abc import ABC, abstractmethod
from typing import AsyncGenerator, Dict, Any, List

class BaseLLMProvider(ABC):
    """Abstract Base Class for LLM Providers (Ollama, Claude, OpenAI, Mock)."""

    @abstractmethod
    async def generate_response(
        self,
        messages: List[Dict[str, str]],
        system_prompt: str,
        temperature: float = 0.3
    ) -> AsyncGenerator[str, None]:
        """Stream response tokens asynchronously."""
        pass

    @abstractmethod
    async def check_health(self) -> Dict[str, Any]:
        """Return connectivity and model availability status."""
        pass
