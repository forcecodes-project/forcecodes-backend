from typing import Annotated

from fastapi import APIRouter, File, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import User, Attempt
from database.session import get_db
from schemas.attempt import AttemptRetrieve
from utils.auth import ActiveUser
from utils.enums import ProgrammingLanguage

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


@router.post("/")
async def new_attempt(
    file: Annotated[bytes, File()],
    user: User = ActiveUser,
    language: ProgrammingLanguage = ProgrammingLanguage.python,
):
    ...
