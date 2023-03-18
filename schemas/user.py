from .base import Schema


class UserRetrieve(Schema):
    id: int
    username: str


class Token(Schema):
    token: str
