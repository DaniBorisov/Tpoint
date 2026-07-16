from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from app.database.database import Base

class Task(Base):

    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(256))
    priority: Mapped[str] = mapped_column(String())
    completed: Mapped[bool] = mapped_column(Boolean, default=False)
