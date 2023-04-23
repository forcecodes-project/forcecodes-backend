from fastapi import Depends, Header, HTTPException
from pydantic import BaseModel
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import User
from database.session import get_db
from schemas.user import NewUser, Token


def hash_password(pwd: str) -> str:
    # XXX: JWT Auth
    return f"{pwd}_1234"


async def get_optional_user(
    token: str | None = Header(default=None), session: AsyncSession = Depends(get_db)
) -> User | None:
    """Returns user or none if not authorized without an exceptions."""
    if not token:
        return None

    try:
        return await get_current_user(token, session)
    except Exception as e:
        return None


async def get_current_user(
    token: str = Header(...), session: AsyncSession = Depends(get_db)
) -> User:
    try:
        username, password = map(str, token.split("_")[:-1])
    except Exception as e:
        raise HTTPException(status_code=403, detail="Wrong token") from e

    # Wtf typing???
    user: User | None = (
        (
            await session.execute(
                select(User).where(
                    User.username == username,
                    User.hashed_password == hash_password(password),
                )
            )
        )
        .scalars()
        .first()
    )
    if not user:
        raise HTTPException(status_code=403, detail="Token expired or malformed")

    return user


class Credentials(BaseModel):
    username: str
    password: str


async def generate_token(
    cred: Credentials, session: AsyncSession = Depends(get_db)
) -> Token:
    user: User | None = (
        (
            await session.execute(
                select(User).where(
                    User.username == cred.username,
                    User.hashed_password == hash_password(cred.password),
                )
            )
        )
        .scalars()
        .first()
    )

    if not user:
        raise HTTPException(status_code=403, detail="Wrong login or password")

    return Token(token=f"{cred.username}_{cred.password}_1234")


async def create_user(
    data: NewUser,
    session: AsyncSession = Depends(get_db),
) -> User:
    if user := (
        await session.execute(select(User).where(User.username == data.username))
    ).one_or_none():
        raise HTTPException(
            status_code=500, detail="User with such username already exists"
        )
    user = User(username=data.username, hashed_password=hash_password(data.password))
    session.add(user)
    await session.commit()
    return user


CreatedUser = Depends(create_user)
ActiveUser = Depends(get_current_user)
OptionalUser = Depends(get_optional_user)
GetToken = Depends(generate_token)
