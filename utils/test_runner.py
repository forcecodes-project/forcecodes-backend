import subprocess
from pathlib import Path

from pydantic import BaseModel


class TestCaseStatus(BaseModel):
    case_id: int
    success: bool
    error: str | None = None


class TestingResult(BaseModel):
    cases: list[TestCaseStatus]
    success: bool


def test_file(path: Path, cases: list[dict]) -> TestingResult:  # noqa
    cases_result = []
    success = True
    for idx, case in enumerate(cases):
        case_id = idx + 1
        with subprocess.Popen(
            ["python", path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            encoding="utf8",
        ) as proc:
            received_output, error = proc.communicate(cases[idx]["test"])

        if error:
            cases_result.append(
                TestCaseStatus(case_id=case_id, success=False, error=error)
            )
            success = False
            continue

        output_lines = received_output.split("\n")[0]
        if output_lines == cases[idx]["result"]:
            cases_result.append(TestCaseStatus(case_id=case_id, success=True))
        else:
            cases_result.append(TestCaseStatus(case_id=case_id, success=False))
            success = False

    return TestingResult(cases=cases_result, success=success)
