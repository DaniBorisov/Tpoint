from sqlalchemy.orm import Session

import logging

from app.schemas.message import MessageCreate
from app.models.message import Message

from app.llm.base import LLMProvider
from app.repositories.message_repository import MessageRepository
from app.services.task_service import TaskService
from app.core.exceptions import LLMUnavailableError, ToolError
from app.tools.registry import ToolRegistry

logger = logging.getLogger(__name__)

HISTORY_LIMIT = 20

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


class MessageService:

    def __init__(
        self,
        repository: MessageRepository,
        task_service: TaskService,
        tool_registry: ToolRegistry,
        llm: LLMProvider,
        max_iterations: int = 5,
    ):
        self.repository = repository
        self.task_service = task_service
        self.tool_registry = tool_registry
        self.llm = llm
        self.max_iterations = max_iterations

    def get_messages(self):
        logger.info("Retrieving all messages")
        return self.repository.get_all()

    def _build_history(self) -> list[dict]:
        past_messages = self.repository.get_all()
        logger.info("Building history from %s messages", len(past_messages))
        recent = past_messages[-HISTORY_LIMIT:]

        history: list[dict] = []
        for m in recent:
            history.append({"role": "user", "content": m.content})
            if m.llm_response:
                history.append({"role": "assistant", "content": m.llm_response})
        return history

    async def _call_llm(
        self,
        messages: list[dict],
        tools: list,
    ):
        logger.info("Calling LLM")
        try:
            return await self.llm.chat_response(
                messages=messages,
                tools=tools,
            )
        except ToolError as e:
            logger.warning("Tool call failed: %s", e)
            raise
        except Exception as e:
            logger.warning("LLM call failed: %s", e)
            raise LLMUnavailableError(f"LLM unavailable: {e}")

    async def create_message(self, message: MessageCreate) -> Message:
        logger.info("Creating message from sender %s", message.sender)
        messages = (
            [SYSTEM_PROMPT]
            + self._build_history()
            + [{"role": "user", "content": message.content}]
        )
        tools = self.tool_registry.get_definitions()

        llm_response = ""
        for iteration in range(self.max_iterations):
            logger.info(
                "Message LLM iteration=%s",
                iteration + 1,
            )

            result = await self._call_llm(messages, tools)

            tool_calls = [
                item
                for item in result.output
                if item["type"] == "function_call"
            ]

            if not tool_calls:
                llm_response = result.output_text
                break

            self.llm.append_assistant_output(messages, result)

            for call in tool_calls:
                logger.info(
                    "Message requested tool=%s",
                    call["name"],
                )
                try:
                    output = self.tool_registry.execute(
                        name=call["name"],
                        arguments=call["arguments"],
                    )
                    tool_output = str(output)
                except ToolError as e:
                    logger.warning("Tool failed: %s", e)
                    tool_output = (
                        "The requested tool could not complete the operation."
                    )

                self.llm.append_tool_output(
                    messages,
                    call_id=call["call_id"],
                    result=tool_output,
                )

        record = Message(
            sender=message.sender,
            content=message.content,
            llm_response=llm_response,
        )

        saved = self.repository.create_message(record)
        logger.info("Message created with id %s", saved.id)
        return saved
