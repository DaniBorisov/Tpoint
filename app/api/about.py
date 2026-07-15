from fastapi import APIRouter

router = APIRouter(
    prefix="/about",
    tags=["About"]
)

@router.get("/")
def about():
    return {"project": "AI assistant",
            "version": "1.0",
            "author": "Daniel"}