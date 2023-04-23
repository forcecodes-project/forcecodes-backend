from enum import Enum


class ProgrammingLanguage(str, Enum):
    python = "Python"


class AttemptStatus(str, Enum):
    pending = "pending"
    failed = "failed"
    success = "success"


class ProblemDiff(str, Enum):
    easy = "easy"
    medium = "medium"
    hard = "hard"
