from .models import session_factory


async def get_db():
    session = session_factory
    try:
        yield session
    finally:
        await session.close()
