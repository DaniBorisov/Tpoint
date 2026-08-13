
import pytest

from app.schemas.task import TaskCreate
from tests.fake_task_repository import FakeTaskRepository
from app.services.task_service import TaskService

from app.models.task import Task

from app.core.exceptions import TaskNotFoundError


def test_get_existing_task():

    repository = FakeTaskRepository()

    service = TaskService(repository) # type: ignore

    repository.tasks[1] = Task(
        id=1,
        title="Learn pytest",
        priority="high",
        completed=False,
    )

    task = service.get_task_db(1)

    assert task.id == 1
    assert task.title == "Learn pytest"
    assert task.priority == "high"

def test_get_missing_task():

    repository = FakeTaskRepository()

    service = TaskService(repository) # type: ignore

    with pytest.raises(
        TaskNotFoundError
    ) as exc_info:

        service.get_task_db(999)

    assert exc_info.value.task_id == 999

def test_create_task():

    repository = FakeTaskRepository()

    service = TaskService(repository) # type: ignore

    task = service.create_task_db(
        TaskCreate(
            title="Write tests",
            priority="high",
            user_id=1,
        )
    )

    assert task.id is not None
    assert task.title == "Write tests"
    assert task.priority == "high"
    assert repository.tasks[task.id] is task

def test_get_tasks_db():

    repository = FakeTaskRepository()

    service = TaskService(repository) # type: ignore

    repository.tasks[1] = Task(
        id=1,
        title="Learn pytest",
        priority="high",
        completed=False,
    )
    repository.tasks[2] = Task(
        id=2,
        title="Study REST",
        priority="low",
        completed=False,
    )

    tasks = service.get_tasks_db()

    assert len(tasks) == 2

def test_get_tasks_db_by_priority():

    repository = FakeTaskRepository()

    service = TaskService(repository) # type: ignore

    repository.tasks[1] = Task(
        id=1,
        title="Learn pytest",
        priority="high",
        completed=False,
    )
    repository.tasks[2] = Task(
        id=2,
        title="Study REST",
        priority="low",
        completed=False,
    )

    high = service.get_tasks_db(priority="high")

    assert len(high) == 1
    assert high[0].title == "Learn pytest"
