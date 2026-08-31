from openai.types.responses import FunctionToolParam


def add_numbers(
    a: float,
    b: float,
) -> float:
    return a + b


ADD_NUMBERS_TOOL: FunctionToolParam = {
    "type": "function",
    "name": "add_numbers",
    "description": "Add two numbers together.",
    "parameters": {
        "type": "object",
        "properties": {
            "a": {
                "type": "number"
            },
            "b": {
                "type": "number"
            },
        },
        "required": [
            "a",
            "b",
        ],
        "additionalProperties": False,
    },
    "strict": True,
}
