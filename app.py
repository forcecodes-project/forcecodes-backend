from fastapi import FastAPI
from loguru import logger

import routers

app = FastAPI(title='Forcecodes Service API')

app.include_router(routers.auth_router)
app.include_router(routers.problems_router)


@app.on_event("startup")
async def startup():
    logger.info("Running service")
