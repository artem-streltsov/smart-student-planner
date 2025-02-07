from telegram import Update
from telegram.ext import ContextTypes
from bot.db.operations import get_lectures_for_today
from bot.services.openai import generate_study_plan
from bot.services.requests import get_events
from bot.config import config
import datetime

async def study_plan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    # Get today's lectures
    lectures = await get_lectures_for_today(user_id)
    
    # Get today's events (from existing events implementation)
    all_events = get_events(config["events"]["url"])
    today_str = datetime.date.today().strftime("%Y-%m-%d")
    today_events = [e for e in all_events if today_str in e.get("time", "")]
    
    # Format input for AI
    lectures_str = "\n".join([f"{lec.name} {lec.start_time}-{lec.end_time} {lec.location}" 
                            for lec in lectures]) if lectures else "No lectures"
    events_str = "\n".join([f"{e['name']} {e['time']} {e['location']}" 
                          for e in today_events]) if today_events else "No events"
    
    print(lectures_str)
    print(events_str)
    
    prompt = f"""
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
    """
    
    plan = await generate_study_plan(prompt)
    
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=plan
    )
