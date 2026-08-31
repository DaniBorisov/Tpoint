import logging
import openai
from openai import OpenAI
from openai.types.responses import FunctionToolParam
import json

from app.core.config import settings
from app.schemas.ai import EmailSummary, PersonInfo
from app.tools import time_tools
from app.tools import math_tools

from app.core.exceptions import LLMAuthenticationError,LLMRateLimitError,LLMProviderError

logger = logging.getLogger(__name__)



time_tool: FunctionToolParam = {
    "type": "function",
    "name": "get_current_time",
    "description": (
        "Get the current local time for a supported city."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "city": {
                "type": "string",
                "description": (
                    "The city whose local time is requested."
                ),
            }
        },
        "required": ["city"],
        "additionalProperties": False,
    },
    "strict": True,
}

add_numbers_tool: FunctionToolParam = {
    "type": "function",
    "name": "add_numbers",
    "description": "Add two numbers together.",
    "parameters": {
        "type": "object",
        "properties": {
            "a": {
                "type": "number"
            },
            "b": {
                "type": "number"
            },
        },
        "required": [
            "a",
            "b",
        ],
        "additionalProperties": False,
    },
    "strict": True,
}

TOOLS = {
    "get_current_time": time_tools.get_current_time,
    "add_numbers": math_tools.add_numbers,
}

class OpenAIProvider:

    def __init__(self):
        self.client = OpenAI(
            api_key=settings.openai_api_key
        )

    def generate(
        self,
        prompt: str,
    ) -> str:

        try:
            response = self.client.responses.create(
                model=settings.openai_model,
                instructions=(
                    "You are an AI assistant. "
                    "Answer clearly and concisely. "
                    "If you do not know something, say so "
                    "rather than inventing information."
                ),
                input=prompt,
            )

            logger.info(
                "OpenAI request completed: response_id=%s",
                response.id,
            )

            logger.debug(
                "LLM response: %s",
                response
            )

            return response.output_text
        
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
            

    def extract_person(
        self,
        text: str,
    ) -> PersonInfo:

        response = self.client.responses.parse(
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

    def summarize_email(
        self,
        email: str,
    ) -> EmailSummary:

        response = self.client.responses.parse(
            model=settings.openai_model,
            input=[
                {
                    "role": "system",
                    "content": (
                        "Analyze the email. "
                        "Summarize its main purpose."
                        "Identify concrete action items."
                        "Determine its priority."
                        "Determine whether the recipient needs to respond."
                        "Only use information present in the email."
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

    def generate_with_tools(
            self,
            prompt:str,
    ):

        try:
            response = self.client.responses.create(
                model=settings.openai_model,
                instructions=(
                                    "You are an AI assistant. "
                                    "Answer clearly and concisely. "
                                    "If you do not know something, say so "
                                    "rather than inventing information."
                                    "If a tools returns something is not supported "
                                    "say that as an response."
                                ),
                input=prompt,
                tools=[time_tool,
                       add_numbers_tool,],
            )

            logger.debug(
                "Tool request raw output: %s",
                response.output,
            )

            input_items = list(response.output)

            function_calls = [
                item
                for item in response.output
                if item.type == "function_call"
            ]

            if not function_calls:
                logger.info(
                    "No tool call requested by model; returning text directly"
                )
                return response.output_text

            for item in function_calls:
                fn = TOOLS[item.name]
                arguments = json.loads(item.arguments)
                logger.info(
                    "Tool called: %s with arguments %s",
                    item.name,
                    arguments,
                )
                result = fn(**arguments)
                logger.info(
                    "Tool result for %s: %s",
                    item.name,
                    result,
                )
                input_items.append(
                    {
                        "type": "function_call_output",
                        "call_id": item.call_id,
                        "output": str(result),
                    }
                )

            final_response = self.client.responses.create(
                model=settings.openai_model,
                input=input_items,
                tools=[time_tool],
            )

            logger.info(
                "Final response after tool call: %s",
                final_response.output_text,
            )

            return final_response.output_text

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


    def create_response(
    self,
    input_items,
    tools,
    ):
        try:
            return self.client.responses.create(
                model=settings.openai_model,
                input=input_items,
                tools=tools,
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