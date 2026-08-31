import asyncio
import httpx
import pytest
from unittest.mock import AsyncMock

from app.models.message import Message
from app.llm.base import LLMResponse
from app.services.message_service import MessageService
from app.tools.registry import ToolRegistry
from tests.fake_message_repository import FakeMessageRepository

from app.schemas.message import MessageCreate
from app.core.exceptions import LLMUnavailableError


def build_service():
    repository = FakeMessageRepository()
    registry = ToolRegistry()
    llm = AsyncMock()
    llm.chat_response = AsyncMock()
    service = MessageService(
        repository=repository,
        task_service=None,  # type: ignore
        tool_registry=registry,
        llm=llm,
    )
    return service, repository, llm


def test_get_messages():

    service, repository, llm = build_service()

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

    service, repository, llm = build_service()
    llm.chat_response = AsyncMock(
        return_value=LLMResponse(output=[], output_text="Hello from LLM")
    )

    saved = asyncio.run(
        service.create_message(
            MessageCreate(sender="user", content="Hi"),
        )
    )

    assert saved.content == "Hi"
    assert saved.llm_response == "Hello from LLM"
    assert repository.messages == [saved]


def test_create_message_llm_unavailable():

    service, repository, llm = build_service()
    llm.chat_response = AsyncMock(
        side_effect=httpx.ConnectError("cannot connect")
    )

    with pytest.raises(LLMUnavailableError):
        asyncio.run(
            service.create_message(
                MessageCreate(sender="user", content="Hi"),
            )
        )
