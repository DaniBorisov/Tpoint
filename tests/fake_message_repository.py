class FakeMessageRepository:

    def __init__(self):
        self.messages = []

    def get_all(self,):
        return self.messages

    def create_message(self, message):
        message.id = len(self.messages) + 1
        self.messages.append(message)
        return message
