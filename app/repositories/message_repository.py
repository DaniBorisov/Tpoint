from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.message import Message

class MessageRepository:

    def __init__(self,
                 db: Session,
                 ):
        self.db = db

    def get_all(self):
        return self.db.scalars(
            select(Message).order_by(Message.id)
        ).all()
    
    def create_message(self, message: Message) -> Message:

        self.db.add(message)
        self.db.commit()
        self.db.refresh(message)

        return message
        