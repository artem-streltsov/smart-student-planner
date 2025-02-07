from telegram import Update
from telegram.ext import ContextTypes
from bot.messages import messages
from bot.config import config
from bot.services.requests import get_events


async def events(update: Update, context: ContextTypes.DEFAULT_TYPE):
    events = get_events(config["events"]["url"] + "/events/")
    if not events:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Sorry, I couldn't find any events right now.",
        )
        return

    # selected_events = random.sample(events, min(3, len(events)))

    for event in events:
        message = f"🎉 <b>{event['name']}</b>\n\n" f"📅 {event['date']}"
        if event["time"]:
            message += f"\n⏰ {event['time']}"
        if event["location"]:
            message += f"\n📍 {event['location']}"
        if event["types"]:
            message += f"\n🏷 {', '.join(event['types'])}"
        if event["description"]:
            message += f"\n📝 {event['description']}"
        message += f"\n\n🔗 <a href='{event['link']}'>More info</a>"
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=message,
            parse_mode="HTML",
            disable_web_page_preview=True,
        )
