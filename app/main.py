from fastapi import FastAPI

from app.api.tasks import router as task_router
from app.api.health import router as health_router
from app.api.about import router as about_router

app = FastAPI()

@app.get("/")
def root():
    return {
        "message": "Welcome to AI assistant"
    }

app.include_router(task_router)
app.include_router(health_router)
app.include_router(about_router)
