import asyncio
import httpx
import pytest
from unittest.mock import AsyncMock, patch

from app.models.message import Message
from tests.fake_message_repository import FakeMessageRepository
from app.services.message_service import MessageService

from app.schemas.message import MessageCreate
from app.core.exceptions import LLMUnavailableError

def test_get_messages():

    repository = FakeMessageRepository()

    service = MessageService(repository=repository, task_service=None) # type: ignore

    repository.messages.append(
        Message(
            id=1,
            sender="user",
            content="Hello",
            llm_response="Hi there",
        )
    )

    messages = service.get_messages()

    assert len(messages) == 1
    assert messages[0].content == "Hello"
    assert messages[0].llm_response == "Hi there"


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


def test_create_message_llm_unavailable():

    repository = FakeMessageRepository()

    service = MessageService(repository=repository, task_service=None) # type: ignore

    with patch("app.services.message_service.get_llm") as mock_get_llm:
        llm = mock_get_llm.return_value
        llm.chat = AsyncMock(
            side_effect=httpx.ConnectError("cannot connect")
        )

        with pytest.raises(LLMUnavailableError):
            asyncio.run(
                service.create_message(
                    MessageCreate(sender="user", content="Hi"),
                )
            )
