from telegram import Update
from telegram.ext import ContextTypes
from bot.messages import messages
from telegram.constants import ParseMode


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=messages["help"],
        parse_mode=ParseMode.HTML,
    )
