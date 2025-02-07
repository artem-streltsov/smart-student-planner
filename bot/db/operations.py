from datetime import time
import logging
import datetime
from sqlalchemy.exc import SQLAlchemyError
from .models.user import User
from .models.lecture import Lecture
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


async def update_ics_url(user_id: int, ics_url: str):
    try:
        with SessionLocal() as session:
            user = session.query(User).filter(User.id == user_id).first()
            if user:
                user.ics_url = ics_url
                session.commit()
                session.refresh(user)
            return user
    except Exception as e:
        logging.error(f"Error updating ICS link for user {user_id}: {e}")
        return None


async def create_lectures(user_id: int, lectures: list):
    try:
        with SessionLocal() as session:
            session.query(Lecture).filter(Lecture.user_id == user_id).delete()
            for lec in lectures:
                new_lecture = Lecture(
                    user_id=user_id,
                    name=lec.get("name"),
                    date=lec.get("date"),
                    start_time=lec.get("start_time"),
                    end_time=lec.get("end_time"),
                    location=lec.get("location"),
                )
                session.add(new_lecture)
            session.commit()
    except Exception as e:
        logging.error(f"Error creating lectures for user {user_id}: {e}")


async def get_lectures_for_today(user_id: int):
    try:
        today_str = datetime.date.today().strftime("%Y-%m-%d")
        with SessionLocal() as session:
            lectures = session.query(Lecture).filter(
                Lecture.user_id == user_id,
                Lecture.date == today_str
            ).all()
            return lectures
    except Exception as e:
        logging.error(f"Error getting lectures for today for user {user_id}: {e}")
        return []
