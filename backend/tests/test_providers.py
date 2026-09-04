import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.providers import get_llm_provider, MockProvider, OllamaProvider, CloudProvider
from app.skills.ship30_writer import build_ship30_prompt

@pytest.mark.asyncio
async def test_provider_factory():
    p_ollama = get_llm_provider("ollama")
    assert isinstance(p_ollama, OllamaProvider)

    p_claude = get_llm_provider("claude")
    assert isinstance(p_claude, CloudProvider)
    assert p_claude.provider_type == "claude"

    p_mock = get_llm_provider("mock")
    assert isinstance(p_mock, MockProvider)

@pytest.mark.asyncio
async def test_mock_streaming():
    mock = MockProvider()
    tokens = []
    async for token in mock.generate_response(
        messages=[{"role": "user", "content": "Tell me about Brian Chesky at Airbnb"}],
        system_prompt="Ground every answer."
    ):
        tokens.append(token)

    full_output = "".join(tokens)
    assert len(full_output) > 50
    assert "Brian Chesky" in full_output
    assert "Airbnb" in full_output

@pytest.mark.asyncio
async def test_ship30_skill_prompt():
    dummy_chunks = [
        {
            "episode": "Brian Chesky's new playbook",
            "guest": "Brian Chesky",
            "timestamp": "00:01:27",
            "text": "We got rid of traditional product management and integrated it with product marketing."
        }
    ]
    prompt = build_ship30_prompt("How did Brian Chesky fix Airbnb?", dummy_chunks)
    assert "Ship 30 for 30" in prompt
    assert "Target Length:" in prompt
    assert "Brian Chesky's new playbook" in prompt
