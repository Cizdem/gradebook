"""Seed script: creates sample students, courses, enrollments, and grades."""

import sys
from pathlib import Path

# Allow running as `python scripts/seed.py` from the project root.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from gradebook import service, storage

DATA_PATH = Path("data/gradebook.json")


def main():
    data = {"students": [], "courses": [], "enrollments": []}

    # Students
    alice_id = service.add_student(data, "Alice Johnson")
    bob_id = service.add_student(data, "Bob Smith")
    carol_id = service.add_student(data, "Carol White")
    print(f"Added students: Alice ({alice_id}), Bob ({bob_id}), Carol ({carol_id})")

    # Courses
    service.add_course(data, "CS101", "Intro to Computer Science")
    service.add_course(data, "MA201", "Calculus I")
    print("Added courses: CS101, MA201")

    # Enrollments
    service.enroll(data, alice_id, "CS101")
    service.enroll(data, alice_id, "MA201")
    service.enroll(data, bob_id, "CS101")
    service.enroll(data, carol_id, "MA201")
    print("Enrolled students in courses.")

    # Grades
    service.add_grade(data, alice_id, "CS101", 92)
    service.add_grade(data, alice_id, "CS101", 88)
    service.add_grade(data, alice_id, "MA201", 75)
    service.add_grade(data, alice_id, "MA201", 81)
    service.add_grade(data, bob_id, "CS101", 70)
    service.add_grade(data, bob_id, "CS101", 65)
    service.add_grade(data, carol_id, "MA201", 95)
    service.add_grade(data, carol_id, "MA201", 98)
    print("Added grades.")

    storage.save_data(data, DATA_PATH)
    print(f"Saved to {DATA_PATH}")


if __name__ == "__main__":
    main()
