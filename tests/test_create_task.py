from tests.fake_task_repository import FakeTaskRepository
from app.services.task_service import TaskService

from app.schemas.task import TaskCreate

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
