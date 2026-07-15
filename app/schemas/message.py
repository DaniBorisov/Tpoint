from pydantic import BaseModel


class MessageCreate(BaseModel):
    sender: str
    content: str


class MessageResponse(BaseModel):
    id: int
    sender: str
    content: str
    timestamp: str
    llm_response: str | None = None
