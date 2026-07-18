from abc import ABC, abstractmethod

class BaseLLM(ABC):

    @abstractmethod
    async def chat(self, prompt: str, history: list[dict] | None = None) -> str:
        ...
