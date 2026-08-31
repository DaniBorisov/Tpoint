from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from app.tools.registry import ToolRegistry


@dataclass
class LLMResponse:
    output: list[dict] = field(default_factory=list)
    output_text: str = ""


GENERIC_INSTRUCTIONS = (
    "You are an AI assistant. "
    "Answer clearly and concisely. "
    "If you do not know something, say so "
    "rather than inventing information."
)


class LLMProvider(ABC):

    def __init__(
        self,
        tool_registry: ToolRegistry,
    ):
        self.tool_registry = tool_registry

    @abstractmethod
    def build_messages(
        self,
        user_message: str,
    ) -> list[dict]:
        ...

    @abstractmethod
    async def chat_response(
        self,
        messages: list[dict],
        tools: list,
    ) -> LLMResponse:
        ...

    @abstractmethod
    def append_assistant_output(
        self,
        messages: list[dict],
        response: LLMResponse,
    ) -> None:
        ...

    @abstractmethod
    def append_tool_output(
        self,
        messages: list[dict],
        call_id: str,
        result: str,
    ) -> None:
        ...
