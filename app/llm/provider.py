from typing import Protocol

from app.schemas.ai import EmailSummary, PersonInfo


class LLMProvider(Protocol):

    def generate(
        self,
        prompt: str,
    ) -> str:
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