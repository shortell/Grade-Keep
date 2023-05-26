import datetime
from decimal import Decimal
import unittest
from server.db import postgres_utils
from server.db import db_utils
from server.db import student


class Test_Student(unittest.TestCase):

    def setUp(self):
        db_utils.initialize_database()
        db_utils.seed_database()

    def test_create_student_successfully(self):
        expected = True
        actual = student.create_student(
            "John", "Smith", "johnSmith123", "password")
        self.assertEqual(actual, expected)

    def test_create_student_failed(self):
        expected = False
        actual = student.create_student(
            'Xanthe', 'Lawson', 'xl123', "password")
        self.assertEqual(actual, expected)

    def test_get_student(self):
        expected = (1, 'Xanthe', 'Lawson', 'xl123')
        actual = student.get_student(1)
        self.assertEqual(actual, expected)

    def test_login_successfully(self):
        actual = student.login('xl123', 'password')
        expected = (1,)
        self.assertEqual(actual, expected)

    def test_login_failed(self):
        actual = student.login('xl123', 'password1')
        expected = None
        self.assertEqual(actual, expected)

    def test_update_student_successfully(self):
        expected = True
        actual = student.update_student(
            1, "John", "Smith", "jsmith64", "password")
        self.assertEqual(actual, expected)

    def test_update_student_failed(self):
        expected = False
        actual = student.update_student(
            2, "John", "Smith", "xl123", "password")
        self.assertEqual(actual, expected)

    def test_delete_student(self):
        query = """
        SELECT COUNT(*) FROM students;
        """
        pre_deletion_count = postgres_utils.exec_get_all(query)[0][0]
        student.delete_student(3, 'password')
        post_deletion_count = postgres_utils.exec_get_all(query)[0][0]
        self.assertEqual(pre_deletion_count, (post_deletion_count + 1))

    def test_get_courses(self):
        expected = [
            (1, 'Algebra I section 01'),
            (2, 'Algebra I section 02')
        ]
        actual = student.get_courses(1)
        self.assertEqual(actual, expected)

    def test_get_course(self):
        expected = (1, 'Algebra I section 01', 'Default course description')
        actual = student.get_course(1)
        self.assertEqual(actual, expected)

    def test_create_submission(self):
        student.create_submission("this is a response", 1, 1)
        query = """
        SELECT id, response, assignment_id, student_id
        FROM submissions
        WHERE id = 7;
        """
        expected = (7, "this is a response", 1, 1)
        actual = postgres_utils.exec_get_one(query)
        self.assertEqual(actual, expected)

    def test_get_submission(self):
        expected = ('Lorem ipsum...', datetime.datetime(
            2004, 10, 19, 10, 23, 54))
        actual = student.get_submission(1, 1)
        self.assertEqual(actual, expected)

    def test_update_submission(self):
        student.update_submission(6, "updated submission")
        query = """
        SELECT id, response, assignment_id, student_id
        FROM submissions
        WHERE id = 6;
        """
        expected = (6, "updated submission", 2, 3)
        actual = postgres_utils.exec_get_one(query)
        self.assertEqual(actual, expected)

    def test_delete_submission(self):
        query = """
        SELECT COUNT(*) FROM submissions;
        """
        pre_deletion_count = postgres_utils.exec_get_all(query)[0][0]
        student.delete_submission(3)
        post_deletion_count = postgres_utils.exec_get_all(query)[0][0]
        self.assertEqual(pre_deletion_count, (post_deletion_count + 1))

    def test_get_score_average_by_course(self):
        expected = (Decimal('0.53750000000000000000'),)
        actual = student.get_score_average_by_course(1, 1)
        self.assertEqual(actual, expected)

    def test_get_grades(self):
        expected = [
            (4,
             'HW#4',
             Decimal('0.90000000000000000000'),
             datetime.datetime(2004, 10, 25, 10, 23, 54)),
            (3,
             'HW#3',
             Decimal('0.75000000000000000000'),
             datetime.datetime(2004, 10, 23, 10, 23, 54)),
            (2,
             'HW#2',
             Decimal('0E-20'),
             datetime.datetime(2004, 10, 21, 10, 23, 54)),
            (1,
             'HW#1',
             Decimal('0.50000000000000000000'),
             datetime.datetime(2004, 10, 19, 10, 23, 54))
        ]
        actual = student.get_grades(1, 1)
        self.assertEqual(actual, expected)

    def test_get_score(self):
        expected = (1, 'HW#1', Decimal('50'), Decimal('100'), '')
        actual = student.get_score(1, 1)
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
