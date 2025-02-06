from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from bot.config import config

# Create the engine
engine = create_engine(config["database"]["sql_uri"], echo=False)

# Create a configured "Session" class
SessionLocal = sessionmaker(bind=engine)
