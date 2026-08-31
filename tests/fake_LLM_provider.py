class FakeResponse:
    def __init__(self, output, output_text=""):
        self.output = output
        self.output_text = output_text


class FakeLLMProvider:

    def __init__(self, responses=None):
        self.responses = list(responses) if responses else []

    def generate(
        self,
        prompt: str,
    ) -> str:
        return "Fake response"

    def generate_with_tools(
        self,
        prompt: str,
    ) -> str:
        return "Fake response"

    def create_response(
        self,
        input_items,
        tools,
    ):
        if not self.responses:
            return FakeResponse(output=[], output_text="Fake response")

        response = self.responses.pop(0)
        return response
