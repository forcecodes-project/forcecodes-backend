from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy import JSON, Column, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import Mapped, declarative_base, mapped_column, relationship
from sqlalchemy.sql import func

from utils.enums import AttemptStatus, ProgrammingLanguage, ProblemDiff

Base = declarative_base()


class BaseSQLAModel(Base):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    ts_created: Mapped[datetime] = mapped_column(nullable=False, default=func.now())


class User(BaseSQLAModel):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]

    def __str__(self):
        return f"<User {self.id}: {self.username}>"


class Problem(BaseSQLAModel):
    __tablename__ = "problems"

    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    title: Mapped[str]
    description: Mapped[str]
    # test_cases = Column(JSONB) TODO: FIX JSONB MAPPED UNDEFINED BEHAVIOUR

    # megabytes
    memory_limit: Mapped[int]
    # seconds
    time_limit: Mapped[int]

    difficulty: Mapped[ProblemDiff] = mapped_column(default=ProblemDiff.easy)

    author: Mapped["User"] = relationship()

    def __str__(self):
        return f"<Problem {self.id}: {self.title}>"


class Attempt(BaseSQLAModel):
    __tablename__ = "attempts"

    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    filename: Mapped[str] = mapped_column(nullable=True)
    language: Mapped[ProgrammingLanguage]
    status: Mapped[AttemptStatus] = mapped_column(default=AttemptStatus.pending)
    problem_id: Mapped[int] = mapped_column(ForeignKey("problems.id"), nullable=False)

    author: Mapped["User"] = relationship()
    problem: Mapped["Problem"] = relationship()

    def __str__(self):
        return f"<Attempt {self.id}: {self.status}>"
