from fastapi import APIRouter, Depends

from app.repositories.task_repository import TaskRepository
from app.schemas.message import MessageCreate, MessageResponse

from app.services.message_service import MessageService
from app.repositories.message_repository import MessageRepository
from app.database.database import get_db

from sqlalchemy.orm import Session

from app.services.task_service import TaskService

def get_task_repository(
        db: Session = Depends(get_db)
):
    return TaskRepository(db)

def get_task_service(
        repository: TaskRepository = Depends(get_task_repository),
        ):
    return TaskService(repository)


def get_message_repositpty(
        db:Session = Depends(get_db)
        ):
    return MessageRepository(db)

def get_message_service(
        repository: MessageRepository = Depends(get_message_repositpty),
        task_service: TaskService = Depends(get_task_service),
        ):
    return MessageService(repository,task_service)


router = APIRouter(
    prefix="/messages",
    tags=["Messages"],
)


@router.get("/", response_model=list[MessageResponse])
def get_messages(service: MessageService = Depends(get_message_service),
                ):
    return service.get_messages()


@router.post("/",response_model=MessageResponse)
async def create_message(message: MessageCreate,
                        service: MessageService = Depends(get_message_service),
                        ):
    return await service.create_message(message)
