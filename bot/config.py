import logging
import os

config = {
    "telegram": {
        "bot_name": "student_planner_bot",
        "api_key": os.getenv("PLANNER_BOT_KEY"),
        "admin": "",
    },
    "database": {
        "sql_uri": os.getenv("DATABASE_URI", "sqlite:///./database.db"),
        "connection_count": 20,
        "overflow_count": 10,
    },
    "logging": {
        "log_level": logging.INFO,
        "debug": False,
    },
    "openai": {
        "api_key": os.getenv("OPENAI_API_TG_KEY"),
    },
    "events": {
        "url": "https://www.kclsu.org",
    },
}
