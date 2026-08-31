import json

from app.llm.base import LLMProvider, LLMResponse
from app.schemas.ai import EmailSummary, PersonInfo
from app.tools.registry import ToolRegistry


class FakeLLMProvider(LLMProvider):

    def __init__(
        self,
        tool_registry: ToolRegistry,
        responses: list[LLMResponse] | None = None,
    ):
        super().__init__(tool_registry)
        self.responses = list(responses) if responses else []
        self.person = PersonInfo(name="Alice", age=32)
        self.summary = EmailSummary(
            summary="Summary",
            priority="low",
            action_items=["a"],
            requires_response=False,
        )

    def build_messages(
        self,
        user_message: str,
    ) -> list[dict]:
        return [
            {"role": "system", "content": "Test"},
            {"role": "user", "content": user_message},
        ]

    async def chat_response(
        self,
        messages: list[dict],
        tools: list,
    ) -> LLMResponse:
        if not self.responses:
            return LLMResponse(output=[], output_text="Fake response")
        return self.responses.pop(0)

    def append_assistant_output(
        self,
        messages: list[dict],
        response: LLMResponse,
    ) -> None:
        for item in response.output:
            if item["type"] == "function_call":
                messages.append(
                    {
                        "type": "function_call",
                        "name": item["name"],
                        "arguments": item["arguments"],
                        "call_id": item["call_id"],
                    }
                )

    def append_tool_output(
        self,
        messages: list[dict],
        call_id: str,
        result: str,
    ) -> None:
        messages.append(
            {
                "type": "function_call_output",
                "call_id": call_id,
                "output": result,
            }
        )

    async def extract_person(
        self,
        text: str,
    ) -> PersonInfo:
        return self.person

    async def summarize_email(
        self,
        email: str,
    ) -> EmailSummary:
        return self.summary


def function_call(
    name: str,
    arguments: dict,
    call_id: str = "call_1",
) -> dict:
    return {
        "type": "function_call",
        "name": name,
        "arguments": json.dumps(arguments),
        "call_id": call_id,
    }
