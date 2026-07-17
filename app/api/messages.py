from fastapi import APIRouter, Depends

from app.schemas.message import MessageCreate, MessageResponse

from app.services.message_service import MessageService
from app.database.database import get_db

from sqlalchemy.orm import Session

def get_message_service():
    return MessageService()


router = APIRouter(
    prefix="/messages",
    tags=["Messages"],
)


@router.get("/", response_model=list[MessageResponse])
def get_messages(service: MessageService = Depends(get_message_service),
                 db: Session =Depends(get_db)):
    return service.get_messages(db)


@router.post("/",response_model=MessageResponse)
async def create_message(message: MessageCreate,
                        service: MessageService = Depends(get_message_service),
                        db:Session = Depends(get_db)):
    return await service.create_message(message, db)
