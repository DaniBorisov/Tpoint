from abc import ABC, abstractmethod

class BaseLLM(ABC):

    @abstractmethod
    async def chat(self, messages: list[dict], tools: list[dict] | None = None) -> dict:
        ...
