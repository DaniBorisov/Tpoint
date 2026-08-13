from fastapi import APIRouter
from fastapi import Depends

from app.schemas.task import TaskCreate, TaskResponse

from app.services.task_service import TaskService
from app.repositories.task_repository import TaskRepository

from sqlalchemy.orm import Session
from app.database.database import get_db

def get_task_repository(
        db: Session = Depends(get_db)
):
    return TaskRepository(db)

def get_task_service(
        repository: TaskRepository = Depends(get_task_repository),
        ):
    return TaskService(repository)


router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
    )

## IN MEMORY 
# @router.get("/", response_model=list[TaskResponse])
# def get_tasks(priority: str | None = None,
#               service: TaskService = Depends(get_task_service)):
#     return service.get_tasks(priority)

# @router.post("/", response_model=TaskResponse)
# def create_task(task: TaskCreate,
#                 service: TaskService = Depends(get_task_service)):
#     return service.create_task(task)

## IN PostgreSQL

@router.get("/db", response_model=list[TaskResponse])
def get_tasks_db( service: TaskService = Depends(get_task_service),
                  priority: str | None = None,):
    return service.get_tasks_db( priority)

@router.get("/db/{task_id}", response_model=TaskResponse)
def get_task_db(task_id: int,
                service: TaskService = Depends(get_task_service),):
    return service.get_task_db(task_id)

@router.post("/db", response_model=TaskResponse)
def create_task_db(
        task: TaskCreate,
        service: TaskService = Depends(get_task_service),
        ):
    return service.create_task_db(task)

## IN memory (dynamic route)

# @router.get("/{task_id}", response_model=TaskResponse)
# def get_task(task_id: int,
#              service: TaskService = Depends(get_task_service)):
#     return service.get_task(task_id)