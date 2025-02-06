import logging
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)

from bot.commands.start import start

from bot.config import config
from bot.commands.help import help
from bot.handlers.misc import unknown, echo


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

application = ApplicationBuilder().token(config["telegram"]["api_key"]).build()

application.add_handler(CommandHandler("start", start))

application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), echo))
