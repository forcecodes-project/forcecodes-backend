from fastapi import APIRouter

router = APIRouter(prefix="/attempts", tags=["User Attempts"])


@router.get("/last")
async def get_last_attempts():
    """Get last 10 user attempts."""
    ...


@router.get("/{id}")
async def get_attempt_details(id: int):
    """Get attempt data by its id."""
    ...
