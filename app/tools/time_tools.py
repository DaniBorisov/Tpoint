from datetime import datetime
from zoneinfo import ZoneInfo

from openai.types.responses import FunctionToolParam


def get_current_time(city: str) -> str:

    timezones = {
        "copenhagen": "Europe/Copenhagen",
        "london": "Europe/London",
        "new york": "America/New_York",
        "sofia": "Europe/Sofia",
    }

    timezone = timezones.get(city.lower())

    if timezone is None:
        return f"Timezone for {city} is not supported."

    current_time = datetime.now(
        ZoneInfo(timezone)
    )

    return current_time.isoformat()


TIME_TOOL: FunctionToolParam = {
    "type": "function",
    "name": "get_current_time",
    "description": (
        "Get the current local time for a supported city."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "city": {
                "type": "string",
                "description": (
                    "The city whose local time is requested."
                ),
            }
        },
        "required": ["city"],
        "additionalProperties": False,
    },
    "strict": True,
}
