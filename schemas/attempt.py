from utils.enums import AttemptStatus, ProgrammingLanguage
from .base import Schema


class AttemptRetrieve(Schema):
    id: int
    author_id: int
    status: AttemptStatus
    language: ProgrammingLanguage
