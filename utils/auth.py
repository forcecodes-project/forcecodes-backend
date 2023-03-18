from fastapi import Depends, Header, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import User
from database.session import get_db
from schemas.user import Token


def hash_password(pwd: str) -> str:
    # XXX: JWT Auth
    return f"{pwd}_1234"


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


ActiveUser = Depends(get_current_user)
GetToken = Depends(generate_token)
