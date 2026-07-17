from app.database.database import Base

from datetime import datetime

from sqlalchemy import String, Text, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

class Message(Base):

    __tablename__ = "messages"

    id:Mapped[int] = mapped_column(primary_key=True)
    sender: Mapped[str] = mapped_column(String())
    content: Mapped[str] = mapped_column(Text)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),)
    llm_response: Mapped[str | None ] = mapped_column(Text, nullable=True)