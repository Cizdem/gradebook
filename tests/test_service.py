"""Unit tests for gradebook.service."""

import unittest
from gradebook import service


def _empty_data():
    return {"students": [], "courses": [], "enrollments": []}


class TestAddStudent(unittest.TestCase):
    """Happy-path and edge cases for add_student."""

    def test_add_student_returns_id(self):
        data = _empty_data()
        sid = service.add_student(data, "Alice")
        self.assertEqual(sid, 1)
        self.assertEqual(len(data["students"]), 1)
        self.assertEqual(data["students"][0].name, "Alice")

    def test_add_multiple_students_increments_id(self):
        data = _empty_data()
        id1 = service.add_student(data, "Alice")
        id2 = service.add_student(data, "Bob")
        self.assertEqual(id1, 1)
        self.assertEqual(id2, 2)

    def test_add_student_empty_name_raises(self):
        data = _empty_data()
        with self.assertRaises(ValueError):
            service.add_student(data, "")

    def test_add_student_whitespace_name_raises(self):
        data = _empty_data()
        with self.assertRaises(ValueError):
            service.add_student(data, "   ")


class TestAddGrade(unittest.TestCase):
    """Happy-path and edge cases for add_grade."""

    def setUp(self):
        self.data = _empty_data()
        self.sid = service.add_student(self.data, "Alice")
        service.add_course(self.data, "CS101", "Intro to CS")
        service.enroll(self.data, self.sid, "CS101")

    def test_add_grade_happy_path(self):
        service.add_grade(self.data, self.sid, "CS101", 95)
        enrollment = self.data["enrollments"][0]
        self.assertIn(95.0, enrollment.grades)

    def test_add_grade_boundary_zero(self):
        service.add_grade(self.data, self.sid, "CS101", 0)
        self.assertIn(0.0, self.data["enrollments"][0].grades)

    def test_add_grade_boundary_hundred(self):
        service.add_grade(self.data, self.sid, "CS101", 100)
        self.assertIn(100.0, self.data["enrollments"][0].grades)

    def test_add_grade_out_of_range_raises(self):
        with self.assertRaises(ValueError):
            service.add_grade(self.data, self.sid, "CS101", 101)

    def test_add_grade_negative_raises(self):
        with self.assertRaises(ValueError):
            service.add_grade(self.data, self.sid, "CS101", -1)

    def test_add_grade_not_enrolled_raises(self):
        service.add_course(self.data, "MA201", "Calculus")
        with self.assertRaises(ValueError):
            service.add_grade(self.data, self.sid, "MA201", 80)


class TestComputeAverage(unittest.TestCase):
    """Happy-path and edge cases for compute_average."""

    def setUp(self):
        self.data = _empty_data()
        self.sid = service.add_student(self.data, "Bob")
        service.add_course(self.data, "CS101", "Intro to CS")
        service.enroll(self.data, self.sid, "CS101")

    def test_compute_average_happy_path(self):
        service.add_grade(self.data, self.sid, "CS101", 80)
        service.add_grade(self.data, self.sid, "CS101", 90)
        avg = service.compute_average(self.data, self.sid, "CS101")
        self.assertAlmostEqual(avg, 85.0)

    def test_compute_average_single_grade(self):
        service.add_grade(self.data, self.sid, "CS101", 72)
        avg = service.compute_average(self.data, self.sid, "CS101")
        self.assertAlmostEqual(avg, 72.0)

    def test_compute_average_no_grades_returns_none(self):
        avg = service.compute_average(self.data, self.sid, "CS101")
        self.assertIsNone(avg)

    def test_compute_average_not_enrolled_raises(self):
        service.add_course(self.data, "PH301", "Physics")
        with self.assertRaises(ValueError):
            service.compute_average(self.data, self.sid, "PH301")


class TestComputeGPA(unittest.TestCase):
    """Tests for compute_gpa."""

    def test_gpa_across_multiple_courses(self):
        data = _empty_data()
        sid = service.add_student(data, "Carol")
        service.add_course(data, "CS101", "Intro to CS")
        service.add_course(data, "MA201", "Calculus")
        service.enroll(data, sid, "CS101")
        service.enroll(data, sid, "MA201")
        service.add_grade(data, sid, "CS101", 80)
        service.add_grade(data, sid, "MA201", 100)
        gpa = service.compute_gpa(data, sid)
        self.assertAlmostEqual(gpa, 90.0)

    def test_gpa_no_grades_returns_none(self):
        data = _empty_data()
        sid = service.add_student(data, "Dave")
        gpa = service.compute_gpa(data, sid)
        self.assertIsNone(gpa)

    def test_gpa_unknown_student_raises(self):
        data = _empty_data()
        with self.assertRaises(ValueError):
            service.compute_gpa(data, 999)


if __name__ == "__main__":
    unittest.main()
