from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import User
from database.session import get_db
from schemas import UserRetrieve

router = APIRouter(prefix="/users", tags=["Users"])


@router.get(
    "/{id}",
    description="Get user data by given id",
    response_model=UserRetrieve,
)
async def get_user_by_id(id: int, session: AsyncSession = Depends(get_db)):
    """Returns user data by given user id."""
    user: User | None = (
        (await session.execute(select(User).where(User.id == id))).scalars().one()
    )

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user
