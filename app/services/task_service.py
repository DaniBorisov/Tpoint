from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlalchemy import select

from app.models.task import Task
from app.schemas.task import TaskCreate

from fastapi import HTTPException

from app.repositories.task_repository import TaskRepository


class TaskService:
    def __init__(self):
        self.repository = TaskRepository()

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
        raise HTTPException(status_code=404, detail="Task Not Found") 
    
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
                      db: Session,
                      priority: str | None = None):
        return self.repository.get_all(db, priority)
    
    def get_task_db(self,
                     db: Session,
                     task_id: int):
        return self.repository.get_task(db, task_id)
       
    
    def create_task_db(self,
                        task_data: TaskCreate,
                        db: Session):

        task = Task(
                title=task_data.title,
                priority=task_data.priority,
             )
        
        return self.repository.create_task(db,task)