from telegram import Update
from telegram.ext import ContextTypes
import logging
from bot.messages import messages
from telegram.constants import ParseMode
from bot.db.operations import get_user, create_user


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /start command by creating a new user if they don't exist."""
    # Extract user information from the update
    telegram_user = update.effective_user
    user_id = telegram_user.id
    first_name = telegram_user.first_name or ""
    last_name = telegram_user.last_name or ""
    username = telegram_user.username or ""

    # Check if the user already exists
    user = await get_user(user_id=user_id)

    if user:
        # User already exists
        logging.info(f"User {user_id} already exists")
        welcome_text = messages["existing_user"].format(name=user.first_name)
    # Create a new user
    else:
        logging.info(f"Creating new user {user_id}")
        await create_user(
            user_id=user_id,
            first_name=first_name,
            last_name=last_name,
            username=username,
        )
        welcome_text = messages["new_user"].format(name=first_name)

    # Send a welcome message
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=welcome_text,
        parse_mode=ParseMode.HTML,
    )
