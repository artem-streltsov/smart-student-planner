from bot.application import application
from bot.handlers.jobs import create_all_jobs

application.job_queue.run_once(create_all_jobs, 0)
application.run_polling()
