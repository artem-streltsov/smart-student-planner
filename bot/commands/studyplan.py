from telegram import Update
from telegram.ext import ContextTypes, CallbackContext
from bot.db.operations import get_lectures_for_today
from bot.services.openai import generate_study_plan
from bot.services.requests import get_events
from bot.config import config
import datetime
from typing import Any
from bot.db.models.lecture import Lecture
from datetime import datetime
import re


async def study_plan(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id: int = update.effective_user.id

    # Get today's lectures
    lectures: list[Lecture] = await get_lectures_for_today(user_id)

    # Get today's events
    all_events: list[dict[str, Any]] = get_events(config["events"]["url"] + "/events")
    today: datetime.date = datetime.today().date()
    print(all_events)
    print("Today: ", today)

    today_events: list[dict[str, Any]] = []
    for event in all_events:
        # Parse date range (e.g. "4th September - 2nd July")
        date_range = event.get("date", "")
        start_str, _, end_str = date_range.partition(" - ")

        # Remove ordinal suffixes and parse dates
        try:
            # todo: compare dates
            today_events.append(event)
        except ValueError:
            continue

    print(today_events)

    # Format input for AI
    lectures_str: str = (
        "\n".join(
            [
                f"{lec.name} {lec.start_time}-{lec.end_time} {lec.location}"
                for lec in lectures
            ]
        )
        if lectures
        else "No lectures"
    )
    events_str: str = (
        "\n".join([f"{e['name']} {e['time']} {e['location']}" for e in today_events])
        if today_events
        else "No events"
    )

    print(lectures_str)
    print(events_str)

    prompt: str = f"""
    Create a daily study plan considering these lectures and events.
    Include suggestions for:
    - Format lectures as
        📚 14:00 - 16:00: Mathematics at Location
    - Format events as
        🎉 16:00 - 18:00: Sport at Location
    - Format meal times such as breakfast, lunch and dinner as
        🍽️ 9:00 - 10:00: Breakfast
    - Format study sessions as
        📖 10:00 - 13:00: Study session

    Use <b></b> tags for bold text. No other formatting. No introduction or conclusion.
    Today's lectures: {lectures_str}
    Today's events: {events_str}
    No events after 22:00
    Don't cram all the events into the day.
    """

    plan: str = await generate_study_plan(prompt)

    await context.bot.send_message(chat_id=update.effective_chat.id, text=plan)
