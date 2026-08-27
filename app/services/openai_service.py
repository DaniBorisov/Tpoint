import logging

from app.llm.provider import LLMProvider

from app.schemas.ai import EmailSummary, PersonInfo


logger = logging.getLogger(__name__)

class OpenAILLMService:

    def __init__(
            self,
            provider: LLMProvider,
    ):
        self.provider = provider
            
    def generate(self, prompt: str) -> str:
        logger.info("Sending request to LLM")

        return self.provider.generate(prompt)

    def extract_person(
        self,
        text: str,
    ) -> PersonInfo:
        return self.provider.extract_person(text)

    def summarize_email(
        self,
        email: str,
    ) -> EmailSummary:
        return self.provider.summarize_email(email)