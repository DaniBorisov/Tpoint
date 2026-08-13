from sqlalchemy.orm import Session

class FakeTaskRepository:

    def __init__(self,):
        self.tasks = {}


    def get_task(
        self,
        task_id: int,
    ):
        return self.tasks.get(task_id)

    def create_task(
        self,
        task,
    ):
        task.id = max(self.tasks.keys(), default=0) + 1

        if task.completed is None:
            task.completed = False

        self.tasks[task.id] = task
        return task