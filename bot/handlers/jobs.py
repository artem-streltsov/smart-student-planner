from telegram.ext import ContextTypes
import logging
from bot.db.operations import get_all_users
from bot.commands.today import today
from datetime import time
from telegram.ext import Application


async def job_callback(context: ContextTypes.DEFAULT_TYPE):
    """
    Wrapper callback for the today command to handle the job context properly.
    """
    print("running job!!")
    await today(None, context)


async def create_user_jobs(context: ContextTypes.DEFAULT_TYPE, user_id: int):
    """
    Creates Telegram bot jobs for the given user to send a message to the user at 9:00 AM every day.
    """
    try:
        # adjust as needed for testing
        job_time = time(14, 16)
        # Schedule the job in the JobQueue to run at specified time every day
        context.job_queue.run_daily(
            job_callback,
            days=(0, 1, 2, 3, 4, 5, 6),
            time=job_time,
            chat_id=user_id,
            name=f"notification_{user_id}_weekday",
            data={user_id},
        )
        logging.info(f"Creating jobs for user {user_id} at {job_time}")
    except Exception as e:
        logging.error(f"Error creating jobs for user {user_id}: {e}")


async def create_all_jobs(application: Application):
    users = await get_all_users()
    print(users)
    for user in users:
        await create_user_jobs(application, user.id)
