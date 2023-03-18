from .base import Schema


class ProblemRetrieve(Schema):
    id: int
    title: str
    description: str
    author_id: int
