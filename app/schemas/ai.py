from pydantic import BaseModel
from enum import Enum


class PersonInfo(BaseModel):
    name: str
    age: int | None


class EmailPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class EmailRequest(BaseModel):
    email: str

class EmailSummary(BaseModel):
    summary: str
    priority: EmailPriority
    action_items: list[str]
    requires_response: bool