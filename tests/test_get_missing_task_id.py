import pytest

from tests.fake_task_repository import FakeTaskRepository
from app.services.task_service import TaskService

from app.core.exceptions import TaskNotFoundError


from app.models.task import Task

def test_get_missing_task():

    repository = FakeTaskRepository()

    service = TaskService(repository) # type: ignore

    with pytest.raises(
        TaskNotFoundError
    ) as exc_info:

        service.get_task_db(999)

    assert exc_info.value.task_id == 999