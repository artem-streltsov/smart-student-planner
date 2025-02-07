import logging
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)

from bot.commands.start import start
from bot.commands.help import help
from bot.commands.set_ics import set_ics
from bot.commands.today import today

from bot.config import config
from bot.handlers.misc import unknown, echo


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

application = ApplicationBuilder().token(config["telegram"]["api_key"]).build()

application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("help", help))
application.add_handler(CommandHandler("setics", set_ics))
application.add_handler(CommandHandler("today", today))

application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), echo))
