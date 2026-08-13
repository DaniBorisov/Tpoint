from unittest.mock import AsyncMock, patch

import httpx

from app.models.message import Message


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
    with patch("app.services.message_service.get_llm") as mock_get_llm:
        llm = mock_get_llm.return_value
        llm.chat = AsyncMock(return_value={"content": "Hello from LLM"})

        response = client.post(
            "/messages/",
            json={"sender": "user", "content": "Hello"},
        )

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
    with patch("app.services.message_service.get_llm") as mock_get_llm:
        llm = mock_get_llm.return_value
        llm.chat = AsyncMock(
            side_effect=httpx.ConnectError("cannot connect")
        )

        response = client.post(
            "/messages/",
            json={"sender": "user", "content": "Hello"},
        )

    assert response.status_code == 502

    data = response.json()

    assert data["error"] == "LLM_UNAVAILABLE"
