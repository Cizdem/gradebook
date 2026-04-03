"""Business logic for the gradebook application."""

import logging
from .models import Student, Course, Enrollment

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _next_student_id(data: dict) -> int:
    """Return the next available student ID."""
    students = data.get("students", [])
    return max((s.id for s in students), default=0) + 1


def _find_student(data: dict, student_id: int) -> Student | None:
    return next((s for s in data["students"] if s.id == student_id), None)


def _find_course(data: dict, course_code: str) -> Course | None:
    return next((c for c in data["courses"] if c.code == course_code), None)


def _find_enrollment(data: dict, student_id: int, course_code: str) -> Enrollment | None:
    return next(
        (
            e
            for e in data["enrollments"]
            if e.student_id == student_id and e.course_code == course_code
        ),
        None,
    )


# ---------------------------------------------------------------------------
# Mutations
# ---------------------------------------------------------------------------

def add_student(data: dict, name: str) -> int:
    """Add a new student and return their assigned ID.

    Args:
        data: the in-memory gradebook dict.
        name: non-empty student name.

    Returns:
        The new student's integer ID.

    Raises:
        ValueError: if name is invalid.
    """
    student_id = _next_student_id(data)
    student = Student(student_id, name)
    data["students"].append(student)
    logger.info("Added student id=%d name=%r", student_id, name)
    return student_id


def add_course(data: dict, code: str, title: str) -> None:
    """Add a new course.

    Raises:
        ValueError: if code/title are invalid or the code already exists.
    """
    if _find_course(data, code):
        raise ValueError(f"Course with code {code!r} already exists.")
    course = Course(code, title)
    data["courses"].append(course)
    logger.info("Added course code=%r title=%r", code, title)


def enroll(data: dict, student_id: int, course_code: str) -> None:
    """Enroll a student in a course.

    Raises:
        ValueError: if student/course not found, or already enrolled.
    """
    if not _find_student(data, student_id):
        raise ValueError(f"Student ID {student_id} not found.")
    if not _find_course(data, course_code):
        raise ValueError(f"Course {course_code!r} not found.")
    if _find_enrollment(data, student_id, course_code):
        raise ValueError(f"Student {student_id} is already enrolled in {course_code!r}.")
    data["enrollments"].append(Enrollment(student_id, course_code))
    logger.info("Enrolled student_id=%d in course=%r", student_id, course_code)


def add_grade(data: dict, student_id: int, course_code: str, grade: float) -> None:
    """Add a grade to a student's enrollment.

    Raises:
        ValueError: if enrollment not found or grade is out of range.
    """
    enrollment = _find_enrollment(data, student_id, course_code)
    if not enrollment:
        raise ValueError(
            f"Student {student_id} is not enrolled in course {course_code!r}."
        )
    enrollment.add_grade(grade)
    logger.info(
        "Added grade %.1f for student_id=%d course=%r", grade, student_id, course_code
    )


# ---------------------------------------------------------------------------
# Queries
# ---------------------------------------------------------------------------

def list_students(data: dict) -> list[dict]:
    """Return all students sorted by name."""
    return [s.to_dict() for s in sorted(data["students"], key=lambda s: s.name)]


def list_courses(data: dict) -> list[dict]:
    """Return all courses sorted by code."""
    return [c.to_dict() for c in sorted(data["courses"], key=lambda c: c.code)]


def list_enrollments(data: dict) -> list[dict]:
    """Return all enrollments sorted by (student_id, course_code)."""
    return [
        e.to_dict()
        for e in sorted(
            data["enrollments"], key=lambda e: (e.student_id, e.course_code)
        )
    ]


def compute_average(data: dict, student_id: int, course_code: str) -> float | None:
    """Return the average grade for a student in a course, or None if no grades."""
    enrollment = _find_enrollment(data, student_id, course_code)
    if not enrollment:
        raise ValueError(
            f"Student {student_id} is not enrolled in course {course_code!r}."
        )
    if not enrollment.grades:
        return None
    return sum(enrollment.grades) / len(enrollment.grades)


def compute_gpa(data: dict, student_id: int) -> float | None:
    """Return the GPA (mean of all course averages) for a student, or None if no grades."""
    if not _find_student(data, student_id):
        raise ValueError(f"Student ID {student_id} not found.")
    enrollments = [e for e in data["enrollments"] if e.student_id == student_id]
    averages = [
        sum(e.grades) / len(e.grades) for e in enrollments if e.grades
    ]
    if not averages:
        return None
    return sum(averages) / len(averages)
