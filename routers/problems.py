from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Problem
from database.session import get_db
from schemas.problem import ProblemRetrieve

router = APIRouter(prefix="/problems", tags=["Problems"])


@router.get(
    "/",
    description="Получение списка всех задач",
    response_model=list[ProblemRetrieve],
)
async def retrieve_problems(session: AsyncSession = Depends(get_db)):
    return (await session.execute(select(Problem))).scalars().all()


@router.get(
    "/{id}",
    description="Получение конкретной задачи по id",
    response_model=ProblemRetrieve,
)
async def retrieve_problem(id: int, session: AsyncSession = Depends(get_db)):
    if (
        problem := (await session.execute(select(Problem).where(Problem.id == id)))
        .scalars()
        .first()
    ):
        return problem
    raise HTTPException(status_code=404, detail="Problem not found")
