import json
import logging
import httpx
from typing import AsyncGenerator, Dict, Any, List
from .base import BaseLLMProvider
from app.config import get_settings

logger = logging.getLogger("lenny_assistant.providers.ollama")
settings = get_settings()

class OllamaProvider(BaseLLMProvider):
    def __init__(self, base_url: str = None, model: str = None):
        self.base_url = (base_url or settings.OLLAMA_BASE_URL).rstrip("/")
        self.model = model or settings.OLLAMA_MODEL
        self.timeout = settings.OLLAMA_TIMEOUT_SECONDS

    async def generate_response(
        self,
        messages: List[Dict[str, str]],
        system_prompt: str,
        temperature: float = 0.3
    ) -> AsyncGenerator[str, None]:
        payload = {
            "model": self.model,
            "messages": [{"role": "system", "content": system_prompt}] + messages,
            "stream": True,
            "options": {"temperature": temperature}
        }

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                async with client.stream("POST", f"{self.base_url}/api/chat", json=payload) as response:
                    if response.status_code != 200:
                        err_text = await response.aread()
                        logger.error(f"Ollama error {response.status_code}: {err_text.decode('utf-8')}")
                        yield f"\n\n**Ollama Error ({response.status_code}):** {err_text.decode('utf-8')}"
                        return

                    async for line in response.aiter_lines():
                        if not line:
                            continue
                        try:
                            chunk = json.loads(line)
                            content = chunk.get("message", {}).get("content", "")
                            if content:
                                yield content
                        except json.JSONDecodeError:
                            continue

        except httpx.ConnectError:
            msg = (
                f"\n\n> [!WARNING]\n"
                f"> **Ollama is unreachable at `{self.base_url}`.**\n>\n"
                f"> To run locally via Ollama:\n"
                f"> 1. Ensure Ollama is installed and running (`ollama serve`).\n"
                f"> 2. Ensure model `{self.model}` is pulled (`ollama pull {self.model}`).\n>\n"
                f"> *Alternatively, switch to the **Cloud Provider** (Claude/OpenAI) or **Demo Mode** in the model selector above.*"
            )
            logger.warning(f"Ollama ConnectError at {self.base_url}")
            yield msg

        except httpx.TimeoutException:
            msg = f"\n\n**Ollama Timeout:** Request to `{self.base_url}` timed out after {self.timeout}s."
            logger.error(msg)
            yield msg

        except Exception as e:
            logger.error(f"Unexpected Ollama exception: {e}")
            yield f"\n\n**Ollama Exception:** {str(e)}"

    async def check_health(self) -> Dict[str, Any]:
        try:
            async with httpx.AsyncClient(timeout=3.0) as client:
                resp = await client.get(f"{self.base_url}/api/tags")
                if resp.status_code == 200:
                    models = [m.get("name") for m in resp.json().get("models", [])]
                    model_ready = any(self.model in m for m in models)
                    return {
                        "status": "healthy" if model_ready else "degraded",
                        "available": True,
                        "base_url": self.base_url,
                        "configured_model": self.model,
                        "model_installed": model_ready,
                        "installed_models": models
                    }
        except Exception as e:
            return {
                "status": "unreachable",
                "available": False,
                "base_url": self.base_url,
                "configured_model": self.model,
                "error": str(e)
            }
