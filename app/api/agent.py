from fastapi import APIRouter, Depends

from app.llm.provider import LLMProvider
from app.llm.openai import OpenAIProvider, time_tool, add_numbers_tool
from app.schemas.agent import (
    AgentRequest,
    AgentResponse,
)
from app.services.agent_service import AgentService
from app.tools.registry import ToolRegistry
from app.tools.time_tools import get_current_time
from app.tools.math_tools import add_numbers


def get_llm_provider() -> LLMProvider:
    return OpenAIProvider()


def get_tool_registry() -> ToolRegistry:

    registry = ToolRegistry()

    registry.register(
        name="get_current_time",
        function=get_current_time,
        definition=time_tool,
    )

    registry.register(
        name="add_numbers",
        function=add_numbers,
        definition=add_numbers_tool,
    )

    return registry


def get_agent_service(
    provider: LLMProvider = Depends(
        get_llm_provider
    ),
    registry: ToolRegistry = Depends(
        get_tool_registry
    ),
) -> AgentService:

    return AgentService(
        llm_provider=provider,
        tool_registry=registry,
    )


router = APIRouter(
    prefix="/agent",
    tags=["Agent"],
)


@router.post(
    "",
    response_model=AgentResponse,
)

def run_agent(
    request: AgentRequest,
    service: AgentService = Depends(
        get_agent_service
    ),
) -> AgentResponse:

    answer = service.run(
        request.message
    )

    return AgentResponse(
        answer=answer
    )