from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.task import Task

class TaskRepository:

    def get_all(
            self,
            db: Session,
            priority: str | None = None,
    ):
        if priority is None:
            return db.scalars(
                select(Task)
            ).all()
        
        return db.scalars(
            select(Task).where(Task.priority == priority)
        ).all()
    
    def get_task(
            self,
            db: Session,
            task_id: int,
             ):
        return db.scalars(
            select(Task).where(Task.id == task_id)
        ).first()
    
    def create_task(
            self,
            db: Session,
            task: Task
    ):
        db.add(task)
        db.commit()
        db.refresh(task)

        return task
    
