from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.message import Message

class MessageRepository:

    def get_all(self, db: Session):
        return db.scalars(
            select(Message).order_by(Message.id)
        ).all()
    
    def create_message(self, db:Session, message: Message) -> Message:

        db.add(message)
        db.commit()
        db.refresh(message)

        return message
        