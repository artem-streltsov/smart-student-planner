from datetime import time
import logging
from sqlalchemy.exc import SQLAlchemyError
from .models.user import User
from .session import SessionLocal
from sqlalchemy.orm import joinedload


async def create_user(user_id: int, first_name: str, last_name: str, username: str):
    try:
        with SessionLocal() as session:
            new_user = User(
                id=user_id,
                first_name=first_name,
                last_name=last_name,
                username=username,
            )
            session.add(new_user)
            session.commit()
            session.refresh(new_user)
            logging.info(f"Created new user with id {new_user.id}")
            return new_user
    except Exception as e:
        logging.error(f"Error creating user with id {user_id}: {e}")
        return None


async def get_user(user_id: int):
    try:
        with SessionLocal() as session:
            user = session.query(User).filter(User.id == user_id).first()
            return user
    except Exception as e:
        logging.error(f"Error getting user with id {user_id}: {e}")
        return None


async def get_all_users():
    try:
        with SessionLocal() as session:
            users = session.query(User).all()
            return users
    except Exception as e:
        logging.error(f"Error getting all users: {e}")
        return None
