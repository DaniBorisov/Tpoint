from functools import partial

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.exceptions import LLMProviderError
from app.database.database import get_db
from app.llm import get_llm
from app.llm.base import LLMProvider
from app.llm.openai import OpenAIProvider
from app.repositories.task_repository import TaskRepository
from app.schemas.agent import AgentRequest, AgentResponse
from app.schemas.ai import EmailRequest, EmailSummary, PersonInfo
from app.services.agent_service import AgentService
from app.services.task_service import TaskService
from app.tools.math_tools import ADD_NUMBERS_TOOL, add_numbers
from app.tools.registry import ToolRegistry
from app.tools.task_tools import CREATE_TASK_TOOL, create_task
from app.tools.time_tools import TIME_TOOL, get_current_time


def get_task_repository(
    db: Session = Depends(get_db),
):
    return TaskRepository(db)


def get_task_service(
    repository: TaskRepository = Depends(get_task_repository),
):
    return TaskService(repository)


def get_tool_registry() -> ToolRegistry:
    registry = ToolRegistry()

    registry.register(
        name="get_current_time",
        function=get_current_time,
        definition=TIME_TOOL,
    )

    registry.register(
        name="add_numbers",
        function=add_numbers,
        definition=ADD_NUMBERS_TOOL,
    )

    return registry


def get_llm_provider(
    registry: ToolRegistry = Depends(get_tool_registry),
) -> LLMProvider:
    return get_llm(tool_registry=registry)


def get_agent_service(
    provider: LLMProvider = Depends(get_llm_provider),
    task_service: TaskService = Depends(get_task_service),
) -> AgentService:
    registry = provider.tool_registry
    registry.register(
        name="create_task",
        function=partial(create_task, task_service),
        definition=CREATE_TASK_TOOL,
    )
    return AgentService(
        llm_provider=provider,
        tool_registry=registry,
    )


def _require_openai(provider: LLMProvider) -> None:
    if not isinstance(provider, OpenAIProvider):
        raise LLMProviderError(
            "This feature is only supported by the OpenAI provider."
        )


router = APIRouter(
    prefix="/agent",
    tags=["Agent"],
)


@router.post(
    "",
    response_model=AgentResponse,
)
async def run_agent(
    request: AgentRequest,
    service: AgentService = Depends(get_agent_service),
) -> AgentResponse:
    answer = await service.run(
        request.message
    )
    return AgentResponse(
        answer=answer
    )


@router.get(
    "/person",
    response_model=PersonInfo,
)
async def person(
    service: AgentService = Depends(get_agent_service),
) -> PersonInfo:
    _require_openai(service.llm_provider)
    return await service.extract_person(
        "Allice us a 32 years old"
    )


@router.post(
    "/summarize-email",
    response_model=EmailSummary,
)
async def email_summarized(
    email: EmailRequest,
    service: AgentService = Depends(get_agent_service),
) -> EmailSummary:
    _require_openai(service.llm_provider)
    return await service.summarize_email(
        email.email
    )
