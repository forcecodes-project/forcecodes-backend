from fastapi import FastAPI
from loguru import logger
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncConnection

import routers
from database.models import Problem, User

app = FastAPI(title="Forcecodes Service API")

app.include_router(routers.auth_router)
app.include_router(routers.problems_router)
app.include_router(routers.users_router)
app.include_router(routers.attempts_router)


@app.on_event("startup")
async def startup():
    logger.info("Running service")

    from database.models import Base
    from database.session import engine

    conn: AsyncConnection
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

        # create test user
        u_q = insert(User).values(
            id=1,
            hashed_password="pass_1234",
            username="test",
        )
        await conn.execute(u_q)

        # create test problem
        q = insert(Problem).values(
            id=1,
            title="A+B",
            description="Return sum of two given numbers",
            # test_cases=json.dumps({
            #     '1': TestCase(input="1 1", output="2").dict(),
            #     '2': TestCase(input="0 -10", output="-10").dict(),
            # }),
            memory_limit=128,
            time_limit=10,
            author_id=1,
        )
        await conn.execute(q)
        q = insert(Problem).values(
            id=2,
            title="A-B",
            description="Return diff of two given numbers",
            # test_cases=json.dumps({
            #     '1': TestCase(input="1 1", output="2").dict(),
            #     '2': TestCase(input="0 -10", output="-10").dict(),
            # }),
            memory_limit=128,
            time_limit=10,
            author_id=1,
        )
        await conn.execute(q)
        await conn.commit()
