from datetime import datetime

from utils.enums import AttemptStatus, ProgrammingLanguage

from .base import Schema


class AttemptRetrieve(Schema):
    id: int
    status: AttemptStatus
    ts_created: datetime

    problem_name: str
