import logging

from app.core.config import settings
from app.llm.base import LLMProvider
from app.llm.ollama import OllamaLLM
from app.llm.openai import OpenAIProvider
from app.tools.registry import ToolRegistry

logger = logging.getLogger(__name__)


def get_llm(
    tool_registry: ToolRegistry | None = None,
) -> LLMProvider:
    provider = settings.llm_provider
    registry = tool_registry or ToolRegistry()

    logger.info("Initializing LLM provider %s", provider)

    if provider == "openai":
        return OpenAIProvider(
            tool_registry=registry,
        )

    if provider == "ollama":
        return OllamaLLM(
            tool_registry=registry,
            base_url=settings.ollama_url,
            model=settings.ollama_model,
            num_ctx=int(settings.ollama_num_ctx),
        )

    raise ValueError(f"Unknown LLM provider: {provider}")
