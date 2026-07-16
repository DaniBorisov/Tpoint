from fastapi import APIRouter
from fastapi import Depends

from app.schemas.task import TaskCreate, TaskResponse

from app.services.task_service import TaskService

from sqlalchemy.orm import Session
from app.database.database import get_db

def get_task_service():
    return TaskService()


router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
    )

## IN MEMORY 
@router.get("/", response_model=list[TaskResponse])
def get_tasks(priority: str | None = None,
              service: TaskService = Depends(get_task_service)):
    return service.get_tasks(priority)

@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: int,
             service: TaskService = Depends(get_task_service)):
    return service.get_task(task_id)

@router.post("/")
def create_task(task: TaskCreate,
                service: TaskService = Depends(get_task_service)):
    return service.create_task(task)

## IN PostgreSQL

@router.get("/db", response_model=list[TaskResponse])
def get_tasks_db(db: Session = Depends(get_db),
                  service: TaskService = Depends(get_task_service),
                  priority: str | None = None,):
    return service.get_tasks_db(db, priority)

@router.get("/db/{task_id}", response_model=TaskResponse)
def get_task_db(task_id: int,
                db: Session = Depends(get_db),
                service: TaskService = Depends(get_task_service),):
    return service.get_task_db(db, task_id)

@router.post("/db")
def create_task_db(
        task: TaskCreate,
        service: TaskService = Depends(get_task_service),
        db: Session = Depends(get_db),
        ):
    return service.create_task_db(task, db)
