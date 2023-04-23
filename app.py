from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncConnection

import routers
from database.models import Problem, User

app = FastAPI(title="Forcecodes Service API")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routers.auth_router)
app.include_router(routers.problems_router)
app.include_router(routers.users_router)
app.include_router(routers.attempts_router)


@app.on_event("startup")
async def startup():
    logger.info("Running service")

    import os

    from database.models import Base
    from database.session import engine

    if not os.path.exists("./tmp"):
        os.mkdir("./tmp")

    return
    conn: AsyncConnection
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        # await conn.run_sync(Base.metadata.create_all)

        # create test user
        u_q = insert(User).values(
            id=1,
            hashed_password="string_1234",
            username="string",
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
