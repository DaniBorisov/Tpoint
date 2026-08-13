from tests.fake_task_repository import FakeTaskRepository
from app.services.task_service import TaskService


from app.models.task import Task

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