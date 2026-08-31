import json

import httpx
import logging

from app.core.exceptions import LLMProviderError
from app.llm.base import GENERIC_INSTRUCTIONS, LLMProvider, LLMResponse
from app.tools.registry import ToolRegistry

logger = logging.getLogger(__name__)

OLLAMA_INSTRUCTIONS = (
    GENERIC_INSTRUCTIONS
    + (
        " Call the create_task tool ONLY when the user is explicitly asking to "
        "create, add, save, or remember a task/to-do/reminder for them to do later. "
        "Otherwise answer directly in plain natural language and never mention "
        "tools. Отговори на въпросите на Български език!"
    )
)


class OllamaLLM(LLMProvider):

    def __init__(
        self,
        tool_registry: ToolRegistry,
        base_url: str,
        model: str,
        num_ctx: int = 4096,
    ):
        super().__init__(tool_registry)
        self.base_url = base_url
        self.model = model
        self.num_ctx = num_ctx

    def build_messages(
        self,
        user_message: str,
    ) -> list[dict]:
        return [
            {
                "role": "system",
                "content": OLLAMA_INSTRUCTIONS,
            },
            {
                "role": "user",
                "content": user_message,
            },
        ]

    async def chat_response(
        self,
        messages: list[dict],
        tools: list,
    ) -> LLMResponse:
        response = await self._chat(messages, tools)
        message = response["message"]

        output: list[dict] = []
        for call in message.get("tool_calls") or []:
            fn = call["function"]
            arguments = fn.get("arguments") or {}
            output.append(
                {
                    "type": "function_call",
                    "name": fn["name"],
                    "arguments": json.dumps(arguments),
                    "call_id": fn.get("name", "call_0"),
                }
            )

        return LLMResponse(
            output=output,
            output_text=message.get("content") or "",
        )

    def append_assistant_output(
        self,
        messages: list[dict],
        response: LLMResponse,
    ) -> None:
        tool_calls = []
        for item in response.output:
            if item["type"] == "function_call":
                tool_calls.append(
                    {
                        "function": {
                            "name": item["name"],
                            "arguments": json.loads(
                                item["arguments"]
                            ),
                        }
                    }
                )

        messages.append(
            {
                "role": "assistant",
                "content": None,
                "tool_calls": tool_calls,
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
                "role": "tool",
                "content": result,
            }
        )

    async def chat(
        self,
        messages: list[dict],
        tools: list[dict] | None = None,
    ) -> dict:
        logger.info(
            "Ollama chat request to %s with model %s (tools=%s)",
            self.base_url,
            self.model,
            bool(tools),
        )
        return await self._chat(messages, tools) # type: ignore

    def _translate_tools(
        self,
        tools: list,
    ) -> list[dict]:
        translated = []
        for tool in tools:
            translated.append(
                {
                    "type": "function",
                    "function": {
                        "name": tool["name"],
                        "description": tool.get("description", ""),
                        "parameters": tool.get("parameters", {}),
                    },
                }
            )
        return translated

    async def _chat(
        self,
        messages: list[dict],
        tools: list,
    ) -> dict:
        payload: dict = {
            "model": self.model,
            "messages": messages,
            "stream": False,
        }

        if tools:
            payload["tools"] = self._translate_tools(tools)

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/api/chat",
                    json=payload,
                    timeout=60.0,
                )
                response.raise_for_status()
        except httpx.HTTPError as exc:
            logger.warning("Ollama request failed: %s", exc)
            raise LLMProviderError(
                "Unable to communicate with the LLM provider."
            ) from exc

        return response.json()
