from pydantic import BaseModel, Field


class AgentRequest(BaseModel):
    message: str = Field(
        min_length=1,
        max_length=10_000,
    )


class AgentResponse(BaseModel):
    answer: str