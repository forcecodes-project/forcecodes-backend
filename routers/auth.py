from fastapi import APIRouter

from database.models import User
from schemas import UserRetrieve
from schemas.user import NewUser, Token
from utils.auth import CreatedUser, GetToken, ActiveUser

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


@router.post(
    "/signup",
    description="Sign Up new user",
    response_model=UserRetrieve,
)
async def signup_user(user: User = CreatedUser):
    return user
