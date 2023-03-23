import pathlib
from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, File, Depends, HTTPException, Body, UploadFile
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import User, Attempt
from database.session import get_db
from schemas.attempt import AttemptRetrieve
from utils.auth import ActiveUser
from utils.enums import ProgrammingLanguage, AttemptStatus
from utils.test_runner import test_file, TestingResult

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
    return (
        (
            await session.execute(
                select(Attempt)
                .where(
                    Attempt.author_id == user.id,
                )
                .limit(10)
            )
        )
        .scalars()
        .all()
    )


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
        status=AttemptStatus.success if result.success else AttemptStatus.failed,
    )

    session.add(attempt)
    await session.commit()

    return result
