from fastapi import FastAPI

from app.api.tasks import router as task_router
from app.api.messages import router as messages_router

app = FastAPI()

@app.get("/")
def root():
    return {"project": "AI assistant exercise",
            "version": "1.0",
            "author": "Daniel"}

app.include_router(task_router)
app.include_router(messages_router)
