from pydantic import BaseModel, ConfigDict

from datetime import datetime

class MessageCreate(BaseModel):
    sender: str
    content: str


class MessageResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    sender: str
    content: str
    timestamp: datetime
    llm_response: str | None = None
