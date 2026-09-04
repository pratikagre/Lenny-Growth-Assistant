import logging
from typing import AsyncGenerator, Dict, Any, List
from .base import BaseLLMProvider
from app.config import get_settings

logger = logging.getLogger("lenny_assistant.providers.cloud")
settings = get_settings()

class CloudProvider(BaseLLMProvider):
    def __init__(self, provider_type: str = "claude"):
        self.provider_type = provider_type.lower()
        self.anthropic_key = settings.ANTHROPIC_API_KEY
        self.openai_key = settings.OPENAI_API_KEY

    async def generate_response(
        self,
        messages: List[Dict[str, str]],
        system_prompt: str,
        temperature: float = 0.3
    ) -> AsyncGenerator[str, None]:
        if self.provider_type == "claude":
            async for token in self._stream_claude(messages, system_prompt, temperature):
                yield token
        elif self.provider_type == "openai":
            async for token in self._stream_openai(messages, system_prompt, temperature):
                yield token
        else:
            yield f"Error: Unsupported cloud provider '{self.provider_type}'."

    async def _stream_claude(
        self,
        messages: List[Dict[str, str]],
        system_prompt: str,
        temperature: float
    ) -> AsyncGenerator[str, None]:
        if not self.anthropic_key:
            yield (
                "\n\n> [!WARNING]\n"
                "> **Anthropic API Key Missing:**\n"
                "> `ANTHROPIC_API_KEY` is not set in `.env`. Please add your key to use Claude 3.5 Sonnet, "
                "or switch to **Ollama** or **Demo Mode**."
            )
            return

        try:
            from anthropic import AsyncAnthropic
            client = AsyncAnthropic(api_key=self.anthropic_key)

            # Format messages for Anthropic API
            formatted_msgs = []
            for m in messages:
                role = "user" if m.get("role") in ["user", "system"] else "assistant"
                formatted_msgs.append({"role": role, "content": m.get("content", "")})

            async with client.messages.stream(
                model=settings.ANTHROPIC_MODEL,
                max_tokens=4096,
                temperature=temperature,
                system=system_prompt,
                messages=formatted_msgs
            ) as stream:
                async for text in stream.text_stream:
                    yield text

        except Exception as e:
            logger.error(f"Claude streaming error: {e}")
            yield f"\n\n**Claude API Error:** {str(e)}"

    async def _stream_openai(
        self,
        messages: List[Dict[str, str]],
        system_prompt: str,
        temperature: float
    ) -> AsyncGenerator[str, None]:
        if not self.openai_key:
            yield (
                "\n\n> [!WARNING]\n"
                "> **OpenAI API Key Missing:**\n"
                "> `OPENAI_API_KEY` is not set in `.env`. Please configure your key to use GPT-4o, "
                "or switch to **Ollama** or **Demo Mode**."
            )
            return

        try:
            from openai import AsyncOpenAI
            client = AsyncOpenAI(api_key=self.openai_key)
            formatted_msgs = [{"role": "system", "content": system_prompt}] + messages

            response = await client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=formatted_msgs,
                temperature=temperature,
                stream=True
            )

            async for chunk in response:
                content = chunk.choices[0].delta.content if chunk.choices else ""
                if content:
                    yield content

        except Exception as e:
            logger.error(f"OpenAI streaming error: {e}")
            yield f"\n\n**OpenAI API Error:** {str(e)}"

    async def check_health(self) -> Dict[str, Any]:
        claude_configured = bool(self.anthropic_key and len(self.anthropic_key) > 8)
        openai_configured = bool(self.openai_key and len(self.openai_key) > 8)
        return {
            "status": "ready" if (claude_configured or openai_configured) else "unconfigured",
            "claude": {
                "configured": claude_configured,
                "model": settings.ANTHROPIC_MODEL
            },
            "openai": {
                "configured": openai_configured,
                "model": settings.OPENAI_MODEL
            }
        }
