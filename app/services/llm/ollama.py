import httpx

from app.services.llm.base import BaseLLM


class OllamaLLM(BaseLLM):

    def __init__(self, base_url: str, model: str):
        self.base_url = base_url
        self.model = model

    async def chat(self, prompt: str) -> str:
        async with httpx.AsyncClient() as client:
            response = await client.post(
            f"{self.base_url}/api/generate",
            json={"model": self.model, "prompt": prompt, "stream": False},
            timeout=60.0,
        )
        response.raise_for_status()
        return response.json()["response"]
