from tests.fake_LLM_provider import FakeLLMProvider
from app.services.openai_service import OpenAILLMService

def test_llm_service():

    provider = FakeLLMProvider()

    service = OpenAILLMService(provider) # type: ignore

    result = service.generate(
        "Hello"
    )

    assert result == "Fake response"
