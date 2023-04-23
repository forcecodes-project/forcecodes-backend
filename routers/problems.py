from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Problem, User
from database.session import get_db
from schemas.problem import ProblemRetrieve
from utils.auth import OptionalUser

router = APIRouter(prefix="/problems", tags=["Problems"])


@router.get(
    "/",
    description="Получение списка всех задач",
    response_model=list[ProblemRetrieve],
)
async def retrieve_problems(
    search: str | None = None,
    user: User | None = OptionalUser,
    session: AsyncSession = Depends(get_db),
):
    if not user:
        return (
            (
                await session.execute(
                    select(Problem).where(Problem.title.like(f"%{search}%"))
                    if search
                    else select(Problem)
                )
            )
            .scalars()
            .all()
        )
    # XXX: Dirty hack to check status of the latest attempt
    query = text(
        f"""
    SELECT id, author_id, title, description, difficulty,
    (
        SELECT status FROM attempts
        WHERE author_id=:author_id and problem_id=problems.id
        ORDER BY ts_created DESC
        LIMIT 1
    )
    FROM problems
    {f"WHERE title LIKE '%{search}%'" if search else ""};
    """
    )
    return (await session.execute(query, dict(author_id=user.id))).mappings().all()


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
