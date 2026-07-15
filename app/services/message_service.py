from datetime import datetime, timezone

from app.schemas.message import MessageCreate
from app.services.llm import get_llm


class MessageService:

    messages: list[dict] = []
    _next_id: int = 1

    def get_messages(self) -> list[dict]:
        return self.messages

    def create_message(self, message: MessageCreate) -> dict:
        llm = get_llm()
        llm_response = llm.chat(message.content)

        record = {
            "id": MessageService._next_id,
            "sender": message.sender,
            "content": message.content,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "llm_response": llm_response,
        }
        MessageService._next_id += 1
        self.messages.append(record)
        return record
