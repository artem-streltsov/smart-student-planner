from telegram import Update
from telegram.ext import ContextTypes
from bot.db.operations import get_lectures_for_today


async def today(update: Update | None, context: ContextTypes.DEFAULT_TYPE):
    """Send today's timetable to the user."""
    # If called from job, use job.chat_id, otherwise use update.effective_chat.id
    if update is None:
        chat_id = context.job.chat_id
        user_id = context.job.data.pop()  # Get user_id from job data
    else:
        chat_id = update.effective_chat.id
        user_id = update.effective_user.id

    lectures = await get_lectures_for_today(user_id)
    if not lectures:
        await context.bot.send_message(
            chat_id=chat_id, text="No lectures scheduled for today."
        )
        return

    message_lines = ["Today's Timetable:\n"]
    for lec in lectures:
        line = (
            f"📚 {lec.name}\n⏰ {lec.start_time} - {lec.end_time}\n📍 {lec.location}\n"
        )
        message_lines.append(line)
    message = "\n".join(message_lines)
    await context.bot.send_message(chat_id=chat_id, text=message)
