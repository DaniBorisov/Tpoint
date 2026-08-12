class AppError(Exception):
    pass


class TaskNotFoundError(AppError):

    def __init__(self, task_id: int):
        self.task_id = task_id

        super().__init__(
            f"Task {task_id} does not exist"
        )


class LLMUnavailableError(AppError):
    pass


class ToolCallError(AppError):
    pass