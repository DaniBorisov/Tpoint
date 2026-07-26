from pydantic import BaseModel, ConfigDict

class TaskCreate(BaseModel):
    title: str 
    priority: str
    user_id: int | None = None

class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    priority: str
    completed: bool
    user_id: int | None