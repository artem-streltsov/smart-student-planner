from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, DateTime, func
import datetime
from ..base import Base


class User(Base):
    """The model for a user."""

    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    first_name: Mapped[str] = mapped_column(String)
    last_name: Mapped[str] = mapped_column(String)
    username: Mapped[str] = mapped_column(String)
    ics_url: Mapped[str] = mapped_column(String, nullable=True)

    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )
