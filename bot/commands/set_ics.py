from telegram import Update
from telegram.ext import ContextTypes
import logging
from bot.db.operations import get_user, update_ics_url, create_lectures
from bot.services.ics_parser import get_ics_from_url, parse_ics

async def set_ics(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if not context.args:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Please provide your ICS link. Usage: /setics <your_ics_link>"
        )
        return

    ics_link = context.args[0]
    user = await get_user(user_id)
    if not user:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="User not found. Please start with /start command first."
        )
        return

    # Save the ICS link to the user record
    user = await update_ics_url(user_id, ics_link)
    if not user:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Failed to update your ICS link. Please try again."
        )
        return

    # Attempt to fetch and parse the ICS file, then store the lectures.
    try:
        ics_text = await get_ics_from_url(ics_link)
        lectures = parse_ics(ics_text)
        await create_lectures(user_id, lectures)
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Your ICS link has been saved and lectures imported."
        )
    except Exception as e:
        logging.error(f"Error processing ICS link for user {user_id}: {e}")
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Error processing your ICS link. Please ensure it is valid and try again."
        )
