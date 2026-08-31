from typing import Protocol

from app.schemas.ai import EmailSummary, PersonInfo


class LLMProvider(Protocol):

    def generate(
        self,
        prompt: str,
    ) -> str:
        ...

    def generate_with_tools(
        self,
        prompt: str,
    ) -> str:
        ...

    def create_response(
        self,
        input_items,
        tools,
    ):
        ...

    def extract_person(
        self,
        text: str,
    ) -> PersonInfo:
        ...

    def summarize_email(
        self,
        email: str,
    ) -> EmailSummary:
        ...