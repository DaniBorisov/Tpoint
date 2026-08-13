from app.models.message import Message
from app.repositories.message_repository import MessageRepository


def test_create_message(db_session):

    repository = MessageRepository(db_session)

    message = Message(
        sender="user",
        content="Integration test",
        llm_response="Hi",
    )

    created = repository.create_message(message)

    assert created.id is not None
    assert created.content == "Integration test"

    db_session.delete(created)
    db_session.commit()

def test_get_all_messages(db_session):

    repository = MessageRepository(db_session)

    message = Message(
        sender="user",
        content="Find me",
        llm_response="Found",
    )

    db_session.add(message)
    db_session.commit()
    db_session.refresh(message)

    messages = repository.get_all()

    assert any(m.id == message.id for m in messages)
    assert any(m.content == "Find me" for m in messages)

    db_session.delete(message)
    db_session.commit()
