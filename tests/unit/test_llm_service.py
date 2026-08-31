import asyncio

from app.llm.base import LLMResponse
from app.services.agent_service import AgentService
from app.tools.registry import ToolRegistry
from tests.fake_LLM_provider import FakeLLMProvider


def test_llm_service_returns_fake_response():
    registry = ToolRegistry()
    provider = FakeLLMProvider(
        tool_registry=registry,
        responses=[LLMResponse(output=[], output_text="Fake response")],
    )
    service = AgentService(
        llm_provider=provider,
        tool_registry=registry,
    )

    result = asyncio.run(service.run("Hello"))

    assert result == "Fake response"
