from pydantic import BaseModel

class TaskCreate(BaseModel):
    title: str 
    priority: str

class TaskResponse(BaseModel):
    id: int
    title: str
    priority: str
    completed: bool