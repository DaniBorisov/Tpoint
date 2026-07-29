from sqlalchemy.orm import Session

import json
import httpx
from fastapi import HTTPException

from app.schemas.message import MessageCreate
from app.schemas.task import TaskCreate
from app.models.message import Message

from app.services.llm import get_llm
from app.repositories.message_repository import MessageRepository
from app.services.task_service import TaskService

HISTORY_LIMIT = 20

CREATE_TASK_TOOL = {
    "type": "function",
    "function": {
        "name": "create_task",
        "description": "Create a new task/todo item for the user.",
        "parameters": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "Short clear decription of the task.",
                },
                "priority": {
                    "type": "string",
                    "enum": ["low","medium", "high"],
                    "description":"What priority the task has",
                },
            },
            "required": ["title","priority"],              
        },
    },
}

SYSTEM_PROMPT = {
    "role": "system",
    "content": ( 
        "The messages below are the real prior conversation with this user, "
        "oldest first - treat them as your actual memory of what was said. "
        "When asked what the user said or asked previously, look at those earlier "
        "messages and answer from them directly; do not claim the conversation "
        "just started unless this is truly the first message.\n\n"
        "You have exactly one tool: create_task. Call it ONLY when the user is "
        "explicitly asking you to create, add, save, or remember a task/to-do/"
        "reminder for them to do later.\n\n"
        "Do NOT call create_task, and do NOT write out JSON, function names, or "
        "call syntax as text, for any of the following: general knowledge "
        "questions, math questions, casual "
        "conversation, or questions about this conversation itself. In all of "
        "these cases just answer directly in plain natural language - never "
        "mention create_task, never suggest the user could call a tool "
        "themselves, and never describe how a tool call would look.\n\n"
        "If you can not answer something, just say you cant do it. "
        "Отговори на въпросите на Български език!"
    ),
}

TOOLS = [CREATE_TASK_TOOL]

class MessageService:

    def __init__(self):
        self.repository = MessageRepository()
        self.task_service = TaskService()

    def get_messages(self, db: Session):
        return self.repository.get_all(db)
    
    def _build_history(self, db: Session) -> list[dict]:
        past_messages = self.repository.get_all(db)
        recent = past_messages[-HISTORY_LIMIT:]

        history: list[dict] = []
        for m in recent:
            history.append({"role": "user", "content": m.content})
            if m.llm_response:
                history.append({"role": "assistant", "content": m.llm_response})
        return history
    
    def _run_tool(self, name: str, arguments: dict, db: Session) -> str:
        if name == "create_task":
            task = self.task_service.create_task_db(
                TaskCreate(
                    title = arguments["title"],
                    priority = arguments["priority"],
                    user_id= 1,
                ),
                db,
            )
            return f"Task created: '{task.title}', '{task.priority}', 'id: {task.id}'"
        return "Unknown tool used"
    
    async def _call_llm(self, lmm, messages: list[dict])-> dict:
        try:
            return await lmm.chat(messages, tools= TOOLS)
        except httpx.HTTPError as e:
            raise HTTPException(status_code=502, detail=f"LLM Unavaliable: {e}")

    async def create_message(self, message: MessageCreate, db: Session) -> Message:
        llm = get_llm()
        history = self._build_history(db)
        messages = [SYSTEM_PROMPT] + history + [{"role": "user", "content": message.content}]

        llm_messages = await self._call_llm(llm, messages)
        tool_calls =  llm_messages.get("tool_calls")

        if tool_calls:
            messages.append(llm_messages)

            for call in tool_calls:
                fn = call["function"]
                name = fn["name"]
                arguments = fn["arguments"]
                if isinstance(arguments, str):
                    arguments = json.loads(arguments)
                
                result = self._run_tool(name, arguments, db)
                messages.append({"role": "tool", "content": result})
            
            final_message = await self._call_llm(llm, messages)
            llm_response = final_message["content"]

        else:
            llm_response = llm_messages["content"]
        
        record = Message(
            sender = message.sender,
            content = message.content,
            llm_response = llm_response,
        )

        return self.repository.create_message(db, record)