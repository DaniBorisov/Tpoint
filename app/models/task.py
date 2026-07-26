from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.user import User

class Task(Base):

    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(256))
    priority: Mapped[str] = mapped_column(String())
    completed: Mapped[bool] = mapped_column(Boolean, default=False)

    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"),
                                                nullable=True)
    
    user: Mapped["User | None"] = relationship(back_populates="tasks",)