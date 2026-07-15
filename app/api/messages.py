from fastapi import APIRouter, Depends

from app.schemas.message import MessageCreate
from app.services.message_service import MessageService


def get_message_service():
    return MessageService()


router = APIRouter(
    prefix="/messages",
    tags=["Messages"],
)


@router.get("/")
def get_messages(service: MessageService = Depends(get_message_service)):
    return service.get_messages()


@router.post("/")
def create_message(message: MessageCreate,
                   service: MessageService = Depends(get_message_service)):
    return service.create_message(message)
