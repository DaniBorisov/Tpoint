import logging
import openai
from openai import OpenAI

from app.core.config import settings
from app.schemas.ai import EmailSummary, PersonInfo

from app.core.exceptions import LLMAuthenticationError,LLMRateLimitError,LLMProviderError

logger = logging.getLogger(__name__)

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