from sqlalchemy.orm import Session

import httpx
from fastapi import HTTPException

from app.schemas.message import MessageCreate
from app.models.message import Message

from app.services.llm import get_llm
from app.repositories.message_repository import MessageRepository

HISTORY_LIMIT = 20

class MessageService:

    def __init__(self):
        self.repository = MessageRepository()

    def get_messages(self, db: Session):
        return self.repository.get_all(db)
    
    def _build_history(self, db: Session) -> list[dict]:
        past_messages = self.repository.get_all(db)
        recent = past_messages[-HISTORY_LIMIT:]

        history: list[dict] = []
        for m in recent:
            history.append({"role": "user", "content": m.content})
            if m.llm_response:
                history.append({"role": "assistant", "content": m.llm_response})
        return history

    async def create_message(self, message: MessageCreate, db: Session) -> Message:
        llm = get_llm()
        history = self._build_history(db)
        try:
            llm_response = await llm.chat(message.content,history=history)
        except httpx.HTTPError as e:
            raise HTTPException(status_code=502, detail="LLM Unavailable {e}")
        
        record = Message(
            sender = message.sender,
            content = message.content,
            llm_response = llm_response,
        )

        return self.repository.create_message(db, record)
