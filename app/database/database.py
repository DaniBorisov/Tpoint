# import os
# from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings


# load_dotenv()

# DATABASE_URL = os.getenv("DATABASE_URL")
# if DATABASE_URL is None:
#     raise RuntimeError("DataBase url is not set")


class Base(DeclarativeBase):
    pass

engine = create_engine(
    settings.database_url,
    echo=settings.database_echo,
    )

SessionLocal = sessionmaker(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
