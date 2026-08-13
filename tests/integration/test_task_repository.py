from app.models.task import Task
from app.repositories.task_repository import TaskRepository


def test_create_task(db_session):

    repository = TaskRepository(db_session)

    task = Task(
        title="Integration test",
        priority="high",
        completed=False,
        user_id=None,
    )

    created_task = repository.create_task(task)

    assert created_task.id is not None
    assert created_task.title == "Integration test"


def test_get_task_by_id(db_session, task_factory):

    repository = TaskRepository(db_session)

    task = task_factory(title="Find me")

    found = repository.get_task(task.id)

    assert found is not None
    assert found.id == task.id
    assert found.title == "Find me"

def test_get_all_tasks(db_session, task_factory):

    repository = TaskRepository(db_session)

    task_factory(title="First", priority="high")
    task_factory(title="Second", priority="low")

    tasks = repository.get_all()

    titles = [t.title for t in tasks]

    assert "First" in titles
    assert "Second" in titles

def test_get_tasks_by_priority(db_session, task_factory):

    repository = TaskRepository(db_session)

    task_factory(title="High task", priority="high")
    task_factory(title="Low task", priority="low")

    high = repository.get_all(priority="high")

    assert all(t.priority == "high" for t in high)
    assert any(t.title == "High task" for t in high)
