from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, ForeignKey
from ..base import Base

class Lecture(Base):
    __tablename__ = "lecture"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"))
    name: Mapped[str] = mapped_column(String, nullable=True)
    date: Mapped[str] = mapped_column(String, nullable=True)
    start_time: Mapped[str] = mapped_column(String, nullable=True)
    end_time: Mapped[str] = mapped_column(String, nullable=True)
    location: Mapped[str] = mapped_column(String, nullable=True)
