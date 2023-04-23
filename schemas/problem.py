from utils.enums import AttemptStatus, ProblemDiff
from .base import Schema


class ProblemRetrieve(Schema):
    id: int
    title: str
    description: str
    author_id: int
    status: AttemptStatus | None = None
    acceptance: int = 100
    difficulty: ProblemDiff = ProblemDiff.easy
