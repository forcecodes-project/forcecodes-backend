from enum import Enum


class ProgrammingLanguage(str, Enum):
    python = "Python"


class AttemptStatus(str, Enum):
    pending = "Pending"
    failed = "Failed"
    success = "Success"
