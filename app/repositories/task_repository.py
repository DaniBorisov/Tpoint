from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.task import Task

class TaskRepository:

    def __init__(self,
                 db: Session,
                 ):
        self.db = db

    def get_all(
            self,
            priority: str | None = None,
    ):
        if priority is None:
            return self.db.scalars(
                select(Task)
            ).all()
        
        return self.db.scalars(
            select(Task).where(Task.priority == priority)
        ).all()
    
    def get_task(
            self,
            task_id: int,
             ):
        return self.db.scalars(
            select(Task).where(Task.id == task_id)
        ).first()
    
    def create_task(
            self,
            task: Task
    ):
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)

        return task
    
