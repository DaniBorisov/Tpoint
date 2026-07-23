import os

from dotenv import load_dotenv

from app.services.llm.base import BaseLLM
from app.services.llm.ollama import OllamaLLM

load_dotenv()


def get_llm() -> BaseLLM:
    provider = os.getenv("LLM_PROVIDER", "ollama")

    if provider == "ollama":
        return OllamaLLM(
            base_url=os.getenv("OLLAMA_URL", "http://localhost:11434"),
            model=os.getenv("OLLAMA_MODEL", "llama3.2"),
            num_ctx = int(os.getenv("OLLAMA_NUM_CTX", "4096" )),
        )

    raise ValueError(f"Unknown LLM provider: {provider}")
