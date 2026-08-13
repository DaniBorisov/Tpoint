# import os

# from dotenv import load_dotenv

import logging

from app.services.llm.base import BaseLLM
from app.services.llm.ollama import OllamaLLM
from app.core.config import settings

# load_dotenv()

logger = logging.getLogger(__name__)


def get_llm() -> BaseLLM:
    provider = settings.llm_provider

    logger.info("Initializing LLM provider %s", provider)

    if provider == "ollama":
        return OllamaLLM(
            base_url=settings.ollama_url,
            model=settings.ollama_model,
            num_ctx = int(settings.ollama_num_ctx),
        )

    raise ValueError(f"Unknown LLM provider: {provider}")
