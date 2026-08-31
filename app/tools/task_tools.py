from openai.types.responses import FunctionToolParam

from app.schemas.task import TaskCreate
from app.services.task_service import TaskService


def create_task(
    task_service: TaskService,
    title: str,
    priority: str,
) -> str:
    task = task_service.create_task_db(
        TaskCreate(
            title=title,
            priority=priority,
            user_id=1,
        )
    )
    return f"Task created: '{task.title}', '{task.priority}', 'id: {task.id}'"


CREATE_TASK_TOOL: FunctionToolParam = {
    "type": "function",
    "name": "create_task",
    "description": "Create a new task/todo item for the user.",
    "parameters": {
        "type": "object",
        "properties": {
            "title": {
                "type": "string",
                "description": "Short clear description of the task.",
            },
            "priority": {
                "type": "string",
                "enum": ["low", "medium", "high"],
                "description": "What priority the task has.",
            },
        },
        "required": ["title", "priority"],
        "additionalProperties": False,
    },
    "strict": True,
}
