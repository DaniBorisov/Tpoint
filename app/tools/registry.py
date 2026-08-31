import json
from typing import Any, Callable

from openai.types.responses import FunctionToolParam

from app.core.exceptions import UnknownToolError

class ToolRegistry:

    def __init__(self):
        self._tools: dict[str, dict] = {}

    def register(
        self,
        name: str,
        function: Callable,
        definition: FunctionToolParam,
    ):
        self._tools[name] = {
            "function": function,
            "definition": definition,
        }

    def get_definitions(self) -> list[FunctionToolParam]:
        return [
            tool["definition"]
            for tool in self._tools.values()
        ]

    def execute(
            self,
            name: str,
            arguments: str,
    ) -> Any:

        tool = self._tools.get(name)

        if tool is None:
            raise UnknownToolError(name)

        parsed_arguments = json.loads(
            arguments
        )

        function = tool["function"]

        return function(
            **parsed_arguments
        )