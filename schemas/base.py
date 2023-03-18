from pydantic import BaseModel


class Schema(BaseModel):
    """Base pydantic ORM mapped schema class."""

    class Config:
        orm_mode = True
