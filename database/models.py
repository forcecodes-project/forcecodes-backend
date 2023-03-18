from __future__ import annotations

import enum
import os
from asyncio import current_task
from datetime import datetime

from sqlalchemy import Boolean, Column, Date, DateTime, Enum, Float, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.asyncio import AsyncSession, async_scoped_session, create_async_engine
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.orm import declarative_base, relationship, sessionmaker, Mapped, mapped_column
from sqlalchemy.sql import func

Base = declarative_base()


class BaseSQLAModel(Base):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    ts_created: Mapped[datetime] = mapped_column(nullable=False, default=func.now())


class User(BaseSQLAModel):
    __tablename__ = 'users'

    username: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]


class Problem(BaseSQLAModel):
    __tablename__ = 'problems'

    author_id: Mapped[int] = mapped_column(nullable=False)
    title: Mapped[str]
    description: Mapped[str]
    test_cases: Mapped[str]

    # megabytes
    memory_limit: Mapped[int]
    # seconds
    time_limit: Mapped[int]
    

connection_string = os.getenv("DB_CONN_STRING", "postgresql+asyncpg://test:test@localhost/test")
engine = create_async_engine(connection_string, echo=False)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)  # noqa
session_factory = async_scoped_session(
    sessionmaker(engine, AsyncSession, autoflush=False, expire_on_commit=False),  # noqa
    scopefunc=current_task,
)
