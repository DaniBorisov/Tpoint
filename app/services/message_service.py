from datetime import datetime, timezone

from app.schemas.message import MessageCreate
from app.services.llm import get_llm

HISTORY_LIMIT = 10


class MessageService:

    messages: list[dict] = []
    _history: dict[str, list[dict]] = {}
    _next_id: int = 1

    def get_messages(self) -> list[dict]:
        return self.messages

    def create_message(self, message: MessageCreate) -> dict:
        sender = message.sender

        if sender not in MessageService._history:
            MessageService._history[sender] = []

        MessageService._history[sender].append({
            "role": "user",
            "content": message.content,
        })

        recent = MessageService._history[sender][-HISTORY_LIMIT * 2:]

        llm = get_llm()
        llm_response = llm.chat(recent)

        MessageService._history[sender].append({
            "role": "assistant",
            "content": llm_response,
        })

        if len(MessageService._history[sender]) > HISTORY_LIMIT * 2:
            MessageService._history[sender] = MessageService._history[sender][-HISTORY_LIMIT * 2:]

        record = {
            "id": MessageService._next_id,
            "sender": sender,
            "content": message.content,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "llm_response": llm_response,
        }
        MessageService._next_id += 1
        self.messages.append(record)
        return record
