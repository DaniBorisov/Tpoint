import ollama

from app.services.llm.base import BaseLLM


class OllamaLLM(BaseLLM):

    def __init__(self, host: str, model: str):
        self.client = ollama.Client(host=host)
        self.model = model

    def chat(self, messages: list[dict]) -> str:
        response = self.client.chat(model=self.model, messages=messages)
        return response["message"]["content"]
