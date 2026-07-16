from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlalchemy import select

from app.models.task import Task
from app.schemas.task import TaskCreate

from fastapi import HTTPException


class TaskService:

    tasks = [
        {
            "id": 1,
            "title": "Learn FastAPI",
            "priority": "high"
        },
        {
            "id": 2,
            "title": "Study REST",
            "priority": "low"
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
        # return [task for task in self.tasks if task["id"] == task_id]
    
    def create_task(self,task):
        # self.tasks.append(task)
        return task
    

    def get_tasks_sql(self,db: Session):
        tasks = db.scalars(
            select(Task)
            ).all()
        return  tasks
       
    
    def create_task_sql(self, task_data: TaskCreate, db: Session):
        task = Task(
                title=task_data.title,
                priority=task_data.priority,
             )
        
        db.add(task)
        db.commit()
        db.refresh(task)
        return task