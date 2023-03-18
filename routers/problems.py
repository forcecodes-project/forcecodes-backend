from fastapi import APIRouter, HTTPException
from pydantic import BaseModel


class TestCase(BaseModel):
    input: str
    output: str


class Problem(BaseModel):
    id: int
    title: str
    description: str
    test_cases: list[TestCase]


problems = [
    Problem(
        id=1,
        title="A+B",
        description="Return sum of two given numbers",
        test_cases=[
            TestCase(input="1 1", output="2"),
            TestCase(input="0 -10", output="-10"),
        ],
    ),
    Problem(
        id=2,
        title="A-B",
        description="Return diff of two given numbers",
        test_cases=[
            TestCase(input="1 1", output="0"),
            TestCase(input="0 -10", output="10"),
        ],
    ),
]

router = APIRouter(prefix="/problems", tags=["Problems"])


@router.get(
    "/",
    description="Получение списка всех задач",
    response_model=list[Problem],
)
async def retrieve_problems():
    return problems


@router.get(
    "/{id}",
    description="Получение конкретной задачи по id",
    response_model=Problem,
)
async def retrieve_problem(id: int):
    try:
        if problem := problems[id - 1]:
            return problem
    except Exception:
        ...
    raise HTTPException(status_code=404, detail="Problem not found")
