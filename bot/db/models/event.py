from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, ARRAY
from ..base import Base


class Event(Base):
    __tablename__ = "event"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    # user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"))
    name: Mapped[str] = mapped_column(String, nullable=True)
    date: Mapped[str] = mapped_column(String, nullable=True)
    # start_time: Mapped[str] = mapped_column(String, nullable=True)
    # end_time: Mapped[str] = mapped_column(String, nullable=True)
    location: Mapped[str] = mapped_column(String, nullable=True)
    description: Mapped[str] = mapped_column(String, nullable=True)
    types: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=True)
    link: Mapped[str] = mapped_column(String, nullable=True)
