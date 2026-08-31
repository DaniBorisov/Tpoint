import logging

import openai
from openai import AsyncOpenAI

from app.core.config import settings
from app.core.exceptions import LLMAuthenticationError, LLMProviderError, LLMRateLimitError
from app.llm.base import GENERIC_INSTRUCTIONS, LLMProvider, LLMResponse
from app.schemas.ai import EmailSummary, PersonInfo
from app.tools.registry import ToolRegistry

logger = logging.getLogger(__name__)

OPENAI_INSTRUCTIONS = (
    GENERIC_INSTRUCTIONS
    + (
        "Call the create_task tool when the user is explicitly asking to "
        "create, add, save, or remember a task/to-do/reminder for them to do later. "
        " If a tool returns something that is not supported, "
        "say that as a response instead of inventing information."
    )
)


class OpenAIProvider(LLMProvider):

    def __init__(
        self,
        tool_registry: ToolRegistry,
    ):
        super().__init__(tool_registry)
        self.client = AsyncOpenAI(
            api_key=settings.openai_api_key
        )

    def build_messages(
        self,
        user_message: str,
    ) -> list[dict]:
        return [
            {
                "role": "system",
                "content": OPENAI_INSTRUCTIONS,
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
        try:
            response = await self.client.responses.create(
                model=settings.openai_model,
                input=messages, # type: ignore
                tools=tools,
            )

            logger.debug(
                "OpenAI raw output: %s",
                response.output,
            )

            output: list[dict] = []
            for item in response.output:
                if item.type == "function_call":
                    output.append(
                        {
                            "type": "function_call",
                            "name": item.name,
                            "arguments": item.arguments,
                            "call_id": item.call_id,
                        }
                    )

            return LLMResponse(
                output=output,
                output_text=response.output_text,
            )

        except openai.RateLimitError as exc:
            raise LLMRateLimitError(
                "The LLM provider rate limit was exceeded."
            ) from exc

        except openai.AuthenticationError as exc:
            raise LLMAuthenticationError(
                "LLM provider authentication failed."
            ) from exc

        except (
            openai.APITimeoutError,
            openai.APIConnectionError,
        ) as exc:
            raise LLMProviderError(
                "Unable to communicate with the LLM provider."
            ) from exc

        except openai.APIError as exc:
            raise LLMProviderError(
                "The LLM provider returned an error."
            ) from exc

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
        response = await self.client.responses.parse(
            model=settings.openai_model,
            input=[
                {
                    "role": "system",
                    "content": (
                        "Extract the person's information "
                        "from the provided text."
                    ),
                },
                {
                    "role": "user",
                    "content": text,
                },
            ],
            text_format=PersonInfo,
        )

        if response.output_parsed is None:
            raise RuntimeError(
                "The model did not return structured output"
            )

        return response.output_parsed

    async def summarize_email(
        self,
        email: str,
    ) -> EmailSummary:
        response = await self.client.responses.parse(
            model=settings.openai_model,
            input=[
                {
                    "role": "system",
                    "content": (
                        "Analyze the email. "
                        "Summarize its main purpose. "
                        "Identify concrete action items. "
                        "Determine its priority. "
                        "Determine whether the recipient needs to respond. "
                        "Only use information present in the email. "
                        "Do not invent action items."
                    ),
                },
                {
                    "role": "user",
                    "content": email,
                },
            ],
            text_format=EmailSummary,
        )

        if response.output_parsed is None:
            raise RuntimeError(
                "The model did not return structured output"
            )

        return response.output_parsed
