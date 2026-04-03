"""Input validation helpers for the CLI."""


def parse_grade(value: str) -> float:
    """Parse and validate a grade string.

    Args:
        value: string representation of a grade.

    Returns:
        Float grade between 0 and 100.

    Raises:
        ValueError: if the value is not a valid number or out of range.
    """
    try:
        grade = float(value)
    except (TypeError, ValueError):
        raise ValueError(f"Grade must be a number, got {value!r}.")
    if not (0 <= grade <= 100):
        raise ValueError(f"Grade must be between 0 and 100, got {grade}.")
    return grade


def parse_student_id(value: str) -> int:
    """Parse and validate a student ID string.

    Raises:
        ValueError: if the value is not a positive integer.
    """
    try:
        sid = int(value)
    except (TypeError, ValueError):
        raise ValueError(f"Student ID must be an integer, got {value!r}.")
    if sid <= 0:
        raise ValueError(f"Student ID must be a positive integer, got {sid}.")
    return sid
