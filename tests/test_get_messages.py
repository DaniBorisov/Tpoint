from tests.fake_message_repository import FakeMessageRepository
from app.services.message_service import MessageService

from app.models.message import Message

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
