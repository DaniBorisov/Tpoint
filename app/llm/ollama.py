import httpx
import logging

from app.llm.base import BaseLLM

logger = logging.getLogger(__name__)


class OllamaLLM(BaseLLM):
    
    def __init__(self, base_url: str, model: str, num_ctx: int = 4096):
        self.base_url = base_url
        self.model = model
        self.num_ctx = num_ctx

    async def chat(self, messages: list[dict], tools: list[dict] | None = None) -> dict:
        logger.info(
            "Ollama chat request to %s with model %s (tools=%s)",
            self.base_url,
            self.model,
            bool(tools),
        )

        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False,
        }

        if tools:
            payload["tools"] = tools


        async with httpx.AsyncClient() as client:
            response = await client.post(
            f"{self.base_url}/api/chat",
            json=payload,
            timeout=60.0,
        )
            
        # print(response.json())
        try:
            response.raise_for_status()
        except httpx.HTTPError as e:
            logger.warning("Ollama request failed: %s", e)
            raise
        return response.json()["message"]
