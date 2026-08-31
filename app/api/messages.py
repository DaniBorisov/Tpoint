from functools import partial

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.llm import get_llm
from app.llm.base import LLMProvider
from app.repositories.task_repository import TaskRepository
from app.schemas.message import MessageCreate, MessageResponse

from app.services.message_service import MessageService
from app.repositories.message_repository import MessageRepository
from app.database.database import get_db

from app.services.task_service import TaskService
from app.tools.registry import ToolRegistry
from app.tools.task_tools import CREATE_TASK_TOOL, create_task


def get_task_repository(
        db: Session = Depends(get_db)
):
    return TaskRepository(db)


def get_task_service(
        repository: TaskRepository = Depends(get_task_repository),
        ):
    return TaskService(repository)


def get_tool_registry(
        task_service: TaskService = Depends(get_task_service),
        ) -> ToolRegistry:
    registry = ToolRegistry()

    registry.register(
        name="create_task",
        function=partial(create_task, task_service),
        definition=CREATE_TASK_TOOL,
    )

    return registry


def get_llm_provider(
        registry: ToolRegistry = Depends(get_tool_registry),
        ) -> LLMProvider:
    return get_llm(tool_registry=registry)


def get_message_repositpty(
        db: Session = Depends(get_db)
        ):
    return MessageRepository(db)


def get_message_service(
        repository: MessageRepository = Depends(get_message_repositpty),
        task_service: TaskService = Depends(get_task_service),
        registry: ToolRegistry = Depends(get_tool_registry),
        llm: LLMProvider = Depends(get_llm_provider),
        ):
    return MessageService(
        repository,
        task_service,
        registry,
        llm,
    )


router = APIRouter(
    prefix="/messages",
    tags=["Messages"],
)


@router.get("/", response_model=list[MessageResponse])
def get_messages(service: MessageService = Depends(get_message_service),
                ):
    return service.get_messages()


@router.post("/", response_model=MessageResponse)
async def create_message(message: MessageCreate,
                        service: MessageService = Depends(get_message_service),
                        ):
    return await service.create_message(message)
