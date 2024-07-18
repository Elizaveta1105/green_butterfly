from datetime import date
import enum

from sqlalchemy import String, DateTime, func, Enum, Boolean, Column, Integer, ForeignKey, Float
from sqlalchemy.orm import declarative_base, mapped_column, Mapped, relationship

Base = declarative_base()


class Role(enum.Enum):
    admin: str = "admin"
    user: str = "user"


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    username: Mapped[str] = mapped_column(String(50), unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(75), nullable=False, unique=True)
    refresh_token: Mapped[str] = mapped_column(String(255), nullable=True)
    created_at: Mapped[date] = mapped_column("created_at", DateTime, default=func.now())
    updated_at: Mapped[date] = mapped_column("updated_at", DateTime, default=func.now(), onupdate=func.now())
    role: Mapped[Enum] = mapped_column("role", Enum(Role), default=Role.admin, nullable=True)
    confirmed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=True)


class Section(Base):
    __tablename__ = "section"
    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String(255), unique=False, nullable=True)
    sum: Mapped[float] = mapped_column(Float())
    sum_currency: Mapped[float] = mapped_column(Float())
    user_id = Column(Integer, ForeignKey("users.id"))
    user: Mapped["User"] = relationship("User", backref="section", lazy="joined")

