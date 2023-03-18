from fastapi import APIRouter
from pydantic import BaseModel

from database.models import User
from schemas import UserRetrieve
from schemas.user import Token
from utils.auth import ActiveUser, GetToken

router = APIRouter(prefix="/auth", tags=["Authorization"])


@router.post(
    "/token",
    description="Get auth Bearer-token",
    response_model=Token,
)
async def get_token(token: Token = GetToken):
    return token


@router.get(
    "/me",
    description="Get current user by token",
    response_model=UserRetrieve,
)
async def retrieve_user(user: User = ActiveUser):
    return user
