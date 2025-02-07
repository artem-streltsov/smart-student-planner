import httpx
from ics import Calendar

async def get_ics_from_url(url: str) -> str:
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.text

def parse_ics(ics_content: str):
    """
    Parses the ICS content and extracts:
      - Lecture name from the line starting with "Description:" in the DESCRIPTION field.
      - Lecture location from the line starting with "Location:" in the DESCRIPTION field.
      - Date field from event start date, formatted as "YYYY-MM-DD".
      - Start and end times formatted as "HH:MM".
    """
    calendar = Calendar(ics_content)
    lectures = []
    for event in calendar.events:
        # Initialize extracted values
        lecture_name = None
        lecture_location = None

        # Extract details from the event description if available.
        if event.description:
            for line in event.description.splitlines():
                if line.startswith("Description:"):
                    lecture_name = line.split(":", 1)[1].strip()
                if line.startswith("Location:"):
                    lecture_location = line.split(":", 1)[1].strip()

        # Format start and end times as "HH:MM"
        start_time = (
            event.begin.datetime.strftime("%H:%M")
            if event.begin and event.begin.datetime
            else None
        )
        end_time = (
            event.end.datetime.strftime("%H:%M")
            if event.end and event.end.datetime
            else None
        )
        # Extract the event date from event.begin, formatted as "YYYY-MM-DD"
        event_date = (
            event.begin.datetime.strftime("%Y-%m-%d")
            if event.begin and event.begin.datetime
            else None
        )

        lectures.append({
            "name": lecture_name,
            "date": event_date,
            "start_time": start_time,
            "end_time": end_time,
            "location": lecture_location,
        })
    return lectures
