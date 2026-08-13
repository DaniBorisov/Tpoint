import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

from fastapi.testclient import TestClient

from app.database.database import get_db
from app.main import app
from app.models.task import Task

from sqlalchemy import delete

from app.models.user import User
from app.models.message import Message


TEST_DATABASE_URL = settings.test_database_url


test_engine = create_engine(
    TEST_DATABASE_URL
)


TestSessionLocal = sessionmaker(
    bind=test_engine,
    autoflush=False,
    autocommit=False,
)

@pytest.fixture
def db_session():

    if not TEST_DATABASE_URL.endswith("ai_assistant_test"):
        raise RuntimeError("Tests must use the test database")

    session = TestSessionLocal()

    try:
        yield session

    finally:
        session.rollback()
        session.close()


@pytest.fixture
def client(db_session):

    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture
def task_factory(db_session):

    def create_task(
        title: str = "Test task",
        priority: str = "medium",
        user_id: int | None = None,
    ):
        task = Task(
            title=title,
            priority=priority,
            completed=False,
            user_id=user_id,
        )

        db_session.add(task)
        db_session.commit()
        db_session.refresh(task)

        return task

    return create_task

@pytest.fixture(autouse=True)
def clean_database(db_session):
    yield

    db_session.execute(delete(Task))
    db_session.execute(delete(Message))
    db_session.execute(delete(User))
    db_session.commit()