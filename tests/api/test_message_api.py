from unittest.mock import AsyncMock

import httpx

from app.llm.base import LLMResponse
from app.main import app
from app.api.messages import get_llm_provider
from app.models.message import Message
from app.tools.registry import ToolRegistry


def _override_provider(**kwargs):
    registry = ToolRegistry()
    provider = AsyncMock()
    provider.tool_registry = registry
    provider.chat_response = AsyncMock(**kwargs)
    app.dependency_overrides[get_llm_provider] = lambda: provider
    return provider


def test_get_messages_api(
    client,
    db_session,
):
    message = Message(
        sender="user",
        content="Hello from the API",
        llm_response="Hi there",
    )

    db_session.add(message)
    db_session.commit()
    db_session.refresh(message)

    response = client.get("/messages/")

    assert response.status_code == 200

    data = response.json()

    assert any(
        m["id"] == message.id
        and m["sender"] == "user"
        and m["content"] == "Hello from the API"
        and m["llm_response"] == "Hi there"
        for m in data
    )

    db_session.delete(message)
    db_session.commit()


def test_create_message_api(
    client,
    db_session,
):
    _override_provider(
        return_value=LLMResponse(output=[], output_text="Hello from LLM")
    )

    try:
        response = client.post(
            "/messages/",
            json={"sender": "user", "content": "Hello"},
        )
    finally:
        app.dependency_overrides.pop(get_llm_provider, None)

    assert response.status_code == 200

    data = response.json()

    assert data["sender"] == "user"
    assert data["content"] == "Hello"
    assert data["llm_response"] == "Hello from LLM"

    created = db_session.get(Message, data["id"])
    db_session.delete(created)
    db_session.commit()


def test_create_message_llm_unavailable_api(
    client,
):
    _override_provider(
        side_effect=httpx.ConnectError("cannot connect")
    )

    try:
        response = client.post(
            "/messages/",
            json={"sender": "user", "content": "Hello"},
        )
    finally:
        app.dependency_overrides.pop(get_llm_provider, None)

    assert response.status_code == 502

    data = response.json()

    assert data["error"] == "LLM_UNAVAILABLE"
