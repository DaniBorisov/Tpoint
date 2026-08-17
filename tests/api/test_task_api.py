from app.models.task import Task


def test_get_task_api(
    client,
    task_factory,
):
    task = task_factory(title="API test task",
                         priority="high")

    response = client.get(
        f"/tasks/db/{task.id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == task.id
    assert data["title"] == "API test task"
    assert data["priority"] == "high"

def test_get_missing_task_api(
    client,
):

    response = client.get(
        "/tasks/db/999999999"
    )

    assert response.status_code == 404

    data = response.json()

    assert data["error"] == "TASK_NOT_FOUND"

def test_get_tasks_api(
    client,
    task_factory,
):
    task = task_factory(title="API test task",
                         priority="high")

    response = client.get(
        f"/tasks/db"
    )

    assert response.status_code == 200

    data = response.json()

    assert any(t["id"] == task.id for t in data)

def test_create_task_api(
    client,
):

    response = client.post(
        "/tasks/db",
        json={"title": "API created task", "priority": "high"},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] is not None
    assert data["title"] == "API created task"
    assert data["priority"] == "high"
    assert data["completed"] is False
