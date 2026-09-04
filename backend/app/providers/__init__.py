from typing import Optional
from .base import BaseLLMProvider
from .ollama_provider import OllamaProvider
from .cloud_provider import CloudProvider
from .mock_provider import MockProvider
from app.config import get_settings

settings = get_settings()

def get_llm_provider(provider_name: Optional[str] = None) -> BaseLLMProvider:
    """
    Dynamic Provider Factory:
    Selects the active LLM provider based on request parameter or default configuration.
    Supported: 'ollama', 'claude', 'openai', 'mock'
    """
    name = (provider_name or settings.DEFAULT_LLM_PROVIDER).lower()

    if name == "ollama":
        return OllamaProvider()
    elif name == "claude":
        return CloudProvider(provider_type="claude")
    elif name == "openai":
        return CloudProvider(provider_type="openai")
    elif name == "mock":
        return MockProvider()
    else:
        # Default fallback
        return OllamaProvider()

__all__ = ["BaseLLMProvider", "OllamaProvider", "CloudProvider", "MockProvider", "get_llm_provider"]
