from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/auth", tags=["Authorization"])


class Credentials(BaseModel):
    username: str
    password: str


class User(BaseModel):
    id: int
    username: str
    hashed_password: str


users = [
    User(id=1, username="user", hashed_password="pass_1234"),
    User(id=2, username="nikolas", hashed_password="pass_1234"),
]


class Token(BaseModel):
    token: str


@router.post(
    "/token",
    description="Get auth Bearer-token",
    response_model=Token,
)
async def get_token(creds: Credentials):
    for user in users:
        if (
            user.username == creds.username
            and user.hashed_password.split("_")[0] == creds.password
        ):
            return Token(token=f"{user.username}_{creds.password}_1234")
    raise HTTPException(status_code=403, detail="Wrong login or password")


@router.get(
    "/me",
    description="Get current user by token",
    response_model=User,
)
async def retrieve_user(token: str = Header(...)):
    try:
        username, password = map(str, token.split("_")[:-1])
    except Exception as e:
        raise HTTPException(status_code=403, detail="Wrong token") from e

    for user in users:
        if user.username == username:
            return user

    raise HTTPException(status_code=403, detail="Invalid token or user not found")
