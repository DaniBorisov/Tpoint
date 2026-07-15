from fastapi import APIRouter
from fastapi import Depends

from app.schemas.task import TaskCreate
from app.services.task_service import TaskService

def get_task_service():
    return TaskService()
# service = TaskService()

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
    )

@router.get("/")
def get_tasks(priority: str | None = None,
              service: TaskService = Depends(get_task_service)):
    return service.get_tasks(priority)

@router.get("/{task_id}")
def get_task(task_id: int,
             service: TaskService = Depends(get_task_service)):
    return service.get_task(task_id)

@router.post("/")
def create_task(task: TaskCreate,
                service: TaskService = Depends(get_task_service)):
    return service.create_task(task)