from datetime import datetime
from zoneinfo import ZoneInfo

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