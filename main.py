"""Command-line interface for the gradebook application."""

import argparse
import inspect
import logging
import sys
import textwrap
from pathlib import Path

from gradebook import service, storage
from gradebook import models
from gradebook.validators import parse_grade, parse_student_id

# ---------------------------------------------------------------------------
# Logging setup
# ---------------------------------------------------------------------------

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "app.log"),
    ],
)
logger = logging.getLogger(__name__)

DATA_PATH = Path("data/gradebook.json")


# ---------------------------------------------------------------------------
# Subcommand handlers
# ---------------------------------------------------------------------------

def cmd_add_student(args, data):
    student_id = service.add_student(data, args.name)
    storage.save_data(data, DATA_PATH)
    print(f"Student added with ID {student_id}: {args.name!r}")


def cmd_add_course(args, data):
    service.add_course(data, args.code, args.title)
    storage.save_data(data, DATA_PATH)
    print(f"Course added: [{args.code}] {args.title}")


def cmd_enroll(args, data):
    student_id = parse_student_id(str(args.student_id))
    service.enroll(data, student_id, args.course)
    storage.save_data(data, DATA_PATH)
    print(f"Student {student_id} enrolled in course {args.course!r}.")


def cmd_add_grade(args, data):
    student_id = parse_student_id(str(args.student_id))
    grade = parse_grade(str(args.grade))
    service.add_grade(data, student_id, args.course, grade)
    storage.save_data(data, DATA_PATH)
    print(f"Grade {grade} added for student {student_id} in {args.course!r}.")


def cmd_list(args, data):
    target = args.target
    if target == "students":
        students = service.list_students(data)
        if not students:
            print("No students found.")
        for s in students:
            print(f"  [{s['id']}] {s['name']}")
    elif target == "courses":
        courses = service.list_courses(data)
        if not courses:
            print("No courses found.")
        for c in courses:
            print(f"  [{c['code']}] {c['title']}")
    elif target == "enrollments":
        enrollments = service.list_enrollments(data)
        if not enrollments:
            print("No enrollments found.")
        for e in enrollments:
            print(
                f"  Student {e['student_id']} -> {e['course_code']}  "
                f"grades={e['grades']}"
            )


def cmd_avg(args, data):
    student_id = parse_student_id(str(args.student_id))
    avg = service.compute_average(data, student_id, args.course)
    if avg is None:
        print(f"No grades recorded for student {student_id} in {args.course!r}.")
    else:
        print(f"Average for student {student_id} in {args.course!r}: {avg:.2f}")


def cmd_gpa(args, data):
    student_id = parse_student_id(str(args.student_id))
    gpa = service.compute_gpa(data, student_id)
    if gpa is None:
        print(f"No grades recorded for student {student_id}.")
    else:
        print(f"GPA for student {student_id}: {gpa:.2f}")


# ---------------------------------------------------------------------------
# Argument parser
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="gradebook",
        description="A simple gradebook manager.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # add-student
    p_add_student = sub.add_parser("add-student", help="Add a new student.")
    p_add_student.add_argument("--name", required=True, help="Student name.")

    # add-course
    p_add_course = sub.add_parser("add-course", help="Add a new course.")
    p_add_course.add_argument("--code", required=True, help="Course code (e.g. CS101).")
    p_add_course.add_argument("--title", required=True, help="Course title.")

    # enroll
    p_enroll = sub.add_parser("enroll", help="Enroll a student in a course.")
    p_enroll.add_argument("--student-id", required=True, type=int)
    p_enroll.add_argument("--course", required=True)

    # add-grade
    p_add_grade = sub.add_parser("add-grade", help="Add a grade for a student.")
    p_add_grade.add_argument("--student-id", required=True, type=int)
    p_add_grade.add_argument("--course", required=True)
    p_add_grade.add_argument("--grade", required=True, type=float)

    # list
    p_list = sub.add_parser("list", help="List students, courses, or enrollments.")
    p_list.add_argument(
        "target",
        choices=["students", "courses", "enrollments"],
    )
    p_list.add_argument("--sort", choices=["name", "code"], default=None, help="Sort key (ignored; sorting is always applied).")

    # avg
    p_avg = sub.add_parser("avg", help="Show average grade for a student in a course.")
    p_avg.add_argument("--student-id", required=True, type=int)
    p_avg.add_argument("--course", required=True)

    # gpa
    p_gpa = sub.add_parser("gpa", help="Show GPA for a student.")
    p_gpa.add_argument("--student-id", required=True, type=int)

    return parser


HANDLERS = {
    "add-student": cmd_add_student,
    "add-course": cmd_add_course,
    "enroll": cmd_enroll,
    "add-grade": cmd_add_grade,
    "list": cmd_list,
    "avg": cmd_avg,
    "gpa": cmd_gpa,
}


def main():
    parser = build_parser()
    args = parser.parse_args()

    data = storage.load_data(DATA_PATH)

    try:
        HANDLERS[args.command](args, data)
    except ValueError as exc:
        logger.error("ValueError in command %r: %s", args.command, exc)
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)
    except KeyError as exc:
        logger.error("KeyError in command %r: %s", args.command, exc)
        print(f"Error: unknown identifier {exc}.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
