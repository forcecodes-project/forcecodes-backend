import os
from asyncio import current_task

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
    create_async_engine,
)
from sqlalchemy.orm import sessionmaker

connection_string = os.getenv(
    "DB_CONN_STRING", "postgresql+asyncpg://test:test@localhost/test"
)
engine = create_async_engine(connection_string, echo=False)
session_factory = async_scoped_session(
    sessionmaker(bind=engine, class_=AsyncSession, autoflush=False, expire_on_commit=False),  # type: ignore
    scopefunc=current_task,
)


async def get_db():
    session = session_factory
    try:
        yield session
    finally:
        await session.close()
