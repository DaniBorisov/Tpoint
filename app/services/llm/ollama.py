import httpx

from app.services.llm.base import BaseLLM


class OllamaLLM(BaseLLM):
    
    def __init__(self, base_url: str, model: str):
        self.base_url = base_url
        self.model = model

    async def chat(self, prompt: str, history: list[dict] | None = None) -> str:
        messages = list(history) if history else []
        messages.append({"role": "user", "content" : prompt})

        async with httpx.AsyncClient() as client:
            response = await client.post(
            f"{self.base_url}/api/chat",
            json={"model": self.model,
                  "messages": messages,
                  "stream": False},
            timeout=60.0,
        )
            
        # print(response.json())
        response.raise_for_status()
        return response.json()["message"]["content"]
