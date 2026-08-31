import json

from app.services.agent_service import AgentService
from app.tools.registry import ToolRegistry
from app.tools.time_tools import get_current_time
from tests.fake_LLM_provider import FakeLLMProvider, FakeResponse


class FakeFunctionCall:
    def __init__(self, name, arguments, call_id="call_1"):
        self.type = "function_call"
        self.name = name
        self.arguments = json.dumps(arguments) if not isinstance(arguments, str) else arguments
        self.call_id = call_id


def build_registry() -> ToolRegistry:
    registry = ToolRegistry()
    registry.register(
        name="get_current_time",
        function=get_current_time,
        definition={
            "type": "function",
            "name": "get_current_time",
            "description": "Get the current local time for a supported city.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string"},
                },
                "required": ["city"],
                "additionalProperties": False,
            },
            "strict": True,
        },
    )
    return registry


def test_agent_returns_text_when_no_tool_call():
    provider = FakeLLMProvider(
        responses=[FakeResponse(output=[], output_text="Plain answer")]
    )
    service = AgentService(
        llm_provider=provider,
        tool_registry=build_registry(),
    )

    result = service.run("Hello")

    assert result == "Plain answer"


def test_agent_executes_tool_and_returns_final_answer():
    call = FakeFunctionCall("get_current_time", {"city": "london"})
    provider = FakeLLMProvider(
        responses=[
            FakeResponse(output=[call]),
            FakeResponse(output=[], output_text="The time in London is 12:00."),
        ]
    )
    service = AgentService(
        llm_provider=provider,
        tool_registry=build_registry(),
    )

    result = service.run("What time is it in London?")

    assert result == "The time in London is 12:00."
