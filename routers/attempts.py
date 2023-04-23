import pathlib
from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Body, Depends, File, HTTPException, UploadFile
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Attempt, User, Problem
from database.session import get_db
from schemas.attempt import AttemptRetrieve
from utils.auth import ActiveUser
from utils.enums import AttemptStatus, ProgrammingLanguage
from utils.test_runner import TestingResult, test_file

router = APIRouter(prefix="/attempts", tags=["User Attempts"])


@router.get(
    "/last",
    response_model=list[AttemptRetrieve],
    description="Get last 10 user attempts",
)
async def get_last_attempts(
    user: User = ActiveUser,
    session: AsyncSession = Depends(get_db),
):
    """Get last 10 user attempts."""
    q = (
        select(
            Attempt.id.label("id"),
            Attempt.status.label("status"),
            Attempt.ts_created.label("ts_created"),
            Problem.title.label("problem_name"),
        )
        .join(Problem)
        .where(
            Attempt.author_id == user.id,
        )
        .limit(10)
    )
    data = (await session.execute(q)).mappings().all()
    print(q)
    return data


@router.get("/{id}")
async def get_attempt_details(
    id: int,
    session: AsyncSession = Depends(get_db),
):
    """Get attempt data by its id."""
    attempt = (
        await session.execute(select(Attempt).where(Attempt.id == id))
    ).scalar_one()
    if not attempt:
        raise HTTPException(status_code=404, detail="Attempt not found")
    return attempt


@router.post(
    "/",
    description="Upload solution to judging",
    response_model=TestingResult,
)
async def new_attempt(
    file: UploadFile = File(...),
    user: User = ActiveUser,
    problem_id: int = Body(..., embed=True),
    session: AsyncSession = Depends(get_db),
):
    path = pathlib.Path(f"./tmp/{problem_id}_{user.id}_{datetime.now().timestamp()}.py")

    with open(path, "wb") as f:
        f.write(await file.read())

    test_cases = [
        {"test": "1 1", "result": "2"},
        {"test": "1 -1", "result": "0"},
        {"test": "1000 1", "result": "1001"},
    ]

    result = test_file(path, cases=test_cases)

    attempt = Attempt(
        author_id=user.id,
        filename="path",
        language=ProgrammingLanguage.python,
        problem_id=problem_id,
        status=AttemptStatus.success if result.success else AttemptStatus.failed,
    )

    session.add(attempt)
    await session.commit()

    return result
