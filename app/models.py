from .database import Base
from sqlalchemy import TIMESTAMP, Boolean, Integer, String, text
from sqlalchemy.orm import Mapped, mapped_column


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    content: Mapped[str] = mapped_column(String, nullable=False)
    publish: Mapped[bool] = mapped_column(
        Boolean, server_default=text("TRUE"), nullable=False
    )
    created_at: Mapped[object] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    email: Mapped[int] = mapped_column(String, unique=True, nullable=False)
    first_name: Mapped[int] = mapped_column(String, nullable=False)
    last_name: Mapped[int] = mapped_column(String, nullable=False)
    created_at: Mapped[object] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
