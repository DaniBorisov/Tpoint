import asyncio
from unittest.mock import AsyncMock, patch

from tests.fake_message_repository import FakeMessageRepository
from app.services.message_service import MessageService

from app.schemas.message import MessageCreate

def test_create_message():

    repository = FakeMessageRepository()

    service = MessageService(repository=repository, task_service=None) # type: ignore

    with patch("app.services.message_service.get_llm") as mock_get_llm:
        llm = mock_get_llm.return_value
        llm.chat = AsyncMock(return_value={"content": "Hello from LLM"})

        saved = asyncio.run(
            service.create_message(
                MessageCreate(sender="user", content="Hi"),
            )
        )

    assert saved.content == "Hi"
    assert saved.llm_response == "Hello from LLM"
    assert repository.messages == [saved]
