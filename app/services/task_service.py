from sqlalchemy.orm import Session

from app.models.task import Task
from app.schemas.task import TaskCreate

from app.repositories.task_repository import TaskRepository
from app.core.exceptions import TaskNotFoundError

import logging

logger = logging.getLogger(__name__)

class TaskService:
    def __init__(self,
                 repository: TaskRepository,
                 ):
        self.repository = repository

## in Memory 

    tasks = [
        {
            "id": 1,
            "title": "Learn FastAPI",
            "priority": "high",
            "completed": False,
        },
        {
            "id": 2,
            "title": "Study REST",
            "priority": "low",
            "completed": False,
        }
    ]

    def get_tasks(self,priority: str | None = None):
        if priority is None:
            return self.tasks  
        return [task for task in self.tasks if task["priority"] == priority]
    
    def get_task(self,task_id: int):       

        for task in self.tasks:
            if task["id"] == task_id:
                return task
        raise TaskNotFoundError(task_id) 
    
    def create_task(self,task):
        next_id = max((t["id"] for t in self.tasks), default=0) + 1
        new_task = {
            "id": next_id,
            "title": task.title,
            "priority": task.priority,
            "completed": False,
            }
        self.tasks.append(new_task)
        return new_task
    

## In PostgreSQL   
#  
    def get_tasks_db(self,
                      priority: str | None = None):

        logger.info(
            "Retrive all tasks",
        )
        
        return self.repository.get_all(priority)
    
    def get_task_db(self,
                     task_id: int):

        logger.info(
            "Retriving task %s",
            task_id,)
        
        task = self.repository.get_task(task_id)


        if task is None:
            logger.warning(
                "Task %s was not found",
                task_id,)

            raise TaskNotFoundError(task_id)
        return task
       
    
    def create_task_db(self,
                        task_data: TaskCreate,
                        ):

        logger.info(
            "Creating Task with priority = %s",
            task_data.priority,)

        task = Task(
                title=task_data.title,
                priority=task_data.priority,
                user_id=task_data.user_id,
             )

        saved = self.repository.create_task(task)

        logger.info(
            "Task created successfully id = %s",
            saved.id,
        )

        return saved