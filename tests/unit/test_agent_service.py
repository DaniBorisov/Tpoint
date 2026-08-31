import asyncio

from app.llm.base import LLMResponse
from app.schemas.ai import EmailSummary, PersonInfo
from app.schemas.task import TaskCreate
from functools import partial

from app.services.agent_service import AgentService
from app.services.task_service import TaskService
from app.tools.registry import ToolRegistry
from app.tools.task_tools import create_task
from tests.fake_LLM_provider import FakeLLMProvider, function_call
from tests.fake_task_repository import FakeTaskRepository


def build_registry() -> ToolRegistry:
    registry = ToolRegistry()
    return registry


def build_service(
    provider_responses: list[LLMResponse] | None = None,
    registry: ToolRegistry | None = None,
) -> AgentService:
    if registry is None:
        registry = build_registry()
    provider = FakeLLMProvider(
        tool_registry=registry,
        responses=provider_responses,
    )
    return AgentService(
        llm_provider=provider,
        tool_registry=registry,
    )


def test_agent_returns_text_when_no_tool_call():
    service = build_service(
        provider_responses=[
            LLMResponse(output=[], output_text="Plain answer")
        ]
    )

    result = asyncio.run(service.run("Hello"))

    assert result == "Plain answer"


def test_agent_executes_tool_and_returns_final_answer():
    call = function_call("get_current_time", {"city": "london"}, call_id="c1")
    service = build_service(
        provider_responses=[
            LLMResponse(output=[call]),
            LLMResponse(output=[], output_text="The time in London is 12:00."),
        ]
    )
    registry = service.tool_registry
    registry.register(
        name="get_current_time",
        function=lambda city: "2026-01-01T12:00:00+00:00",
        definition={
            "type": "function",
            "name": "get_current_time",
            "description": "Get the current local time.",
            "parameters": {
                "type": "object",
                "properties": {"city": {"type": "string"}},
                "required": ["city"],
            },
            "strict": True,
        },
    )

    result = asyncio.run(service.run("What time is it in London?"))

    assert result == "The time in London is 12:00."


def test_agent_creates_task_via_tool():
    call = function_call(
        "create_task",
        {"title": "Buy milk", "priority": "high"},
        call_id="c1",
    )
    repo = FakeTaskRepository()
    task_service = TaskService(repo)

    registry = build_registry()
    registry.register(
        name="create_task",
        function=partial(create_task, task_service),
        definition={},
    )

    provider = FakeLLMProvider(
        tool_registry=registry,
        responses=[
            LLMResponse(output=[call]),
            LLMResponse(output=[], output_text="Task created."),
        ],
    )
    service = AgentService(
        llm_provider=provider,
        tool_registry=registry,
    )

    result = asyncio.run(service.run("Please create a task to buy milk with high priority"))

    assert result == "Task created."
    assert list(repo.tasks.values())[0].title == "Buy milk"


def test_agent_extract_person():
    service = build_service()

    person = asyncio.run(service.extract_person("Alice is 32"))

    assert person == PersonInfo(name="Alice", age=32)


def test_agent_summarize_email():
    service = build_service()

    summary = asyncio.run(
        service.summarize_email("Please review the document.")
    )

    assert summary == EmailSummary(
        summary="Summary",
        priority="low",
        action_items=["a"],
        requires_response=False,
    )
