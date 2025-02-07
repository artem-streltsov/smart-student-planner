from .base import Base
from .session import engine
from .models.user import User
from .models.lecture import Lecture


def init_db():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()
