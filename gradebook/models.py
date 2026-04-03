"""Core data models for the gradebook application."""


class Student:
    """Represents a student with an ID and name."""

    def __init__(self, student_id: int, name: str):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Student name must be a non-empty string.")
        self.id = student_id
        self.name = name.strip()

    def to_dict(self) -> dict:
        return {"id": self.id, "name": self.name}

    @classmethod
    def from_dict(cls, data: dict) -> "Student":
        return cls(data["id"], data["name"])

    def __str__(self) -> str:
        return f"Student(id={self.id}, name={self.name!r})"

    def __repr__(self) -> str:
        return self.__str__()


class Course:
    """Represents a course with a code and title."""

    def __init__(self, code: str, title: str):
        if not isinstance(code, str) or not code.strip():
            raise ValueError("Course code must be a non-empty string.")
        if not isinstance(title, str) or not title.strip():
            raise ValueError("Course title must be a non-empty string.")
        self.code = code.strip()
        self.title = title.strip()

    def to_dict(self) -> dict:
        return {"code": self.code, "title": self.title}

    @classmethod
    def from_dict(cls, data: dict) -> "Course":
        return cls(data["code"], data["title"])

    def __str__(self) -> str:
        return f"Course(code={self.code!r}, title={self.title!r})"

class Enrollment:
    """Represents a student's enrollment in a course, including their grades."""

    def __init__(self, student_id: int, course_code: str, grades: list = None):
        self.student_id = student_id
        self.course_code = course_code
        self.grades: list[float] = []
        for g in (grades or []):
            self._validate_and_add(g)

    def _validate_and_add(self, grade):
        grade = float(grade)
        if not (0 <= grade <= 100):
            raise ValueError(f"Grade must be between 0 and 100, got {grade}.")
        self.grades.append(grade)

    def add_grade(self, grade) -> None:
        """Add a validated grade to this enrollment."""
        self._validate_and_add(grade)

    def to_dict(self) -> dict:
        return {
            "student_id": self.student_id,
            "course_code": self.course_code,
            "grades": self.grades,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Enrollment":
        return cls(data["student_id"], data["course_code"], data.get("grades", []))

    def __str__(self) -> str:
        return (
            f"Enrollment(student_id={self.student_id}, "
            f"course_code={self.course_code!r}, grades={self.grades})"
        )

    def __repr__(self) -> str:
        return self.__str__()
