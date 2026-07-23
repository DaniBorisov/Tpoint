import httpx

from app.services.llm.base import BaseLLM


class OllamaLLM(BaseLLM):
    
    def __init__(self, base_url: str, model: str, num_ctx: int = 4096):
        self.base_url = base_url
        self.model = model
        self.num_ctx = num_ctx

    async def chat(self, messages: list[dict], tools: list[dict] | None = None) -> dict:
        # messages = list(history) if history else []
        # messages.append({"role": "user", "content" : prompt})

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
        response.raise_for_status()
        return response.json()["message"]
