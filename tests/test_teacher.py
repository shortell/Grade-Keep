from decimal import Decimal
import unittest
import datetime
from server.db import postgres_utils
from server.db import db_utils
from server.db import teacher


class Test_Teacher(unittest.TestCase):

    def setUp(self):
        db_utils.initialize_database()
        db_utils.seed_database()

    def test_create_teacher_successfully(self):
        actual = teacher.create_teacher(
            "John", "Smith", "johnSmith123", "password")
        expected = True
        self.assertEqual(actual, expected)

    def test_create_teacher_failed(self):
        actual = teacher.create_teacher(
            "Sidney", "Velazquez", "sv123", "password")
        expected = False
        self.assertEqual(actual, expected)

    def test_get_teacher(self):
        expected = (1, 'Sidney', 'Velazquez', 'sv123')
        actual = teacher.get_teacher(1)
        self.assertEqual(actual, expected)

    def test_login_successfully(self):
        actual = teacher.login('sv123', 'password')
        expected = (1,)
        self.assertEqual(actual, expected)

    def test_login_failed(self):
        actual = teacher.login('sv124', 'password1')
        expected = None
        self.assertEqual(actual, expected)

    def test_update_teacher_successfully(self):
        expected = True
        actual = teacher.update_teacher(
            1, "John", "Smith", "jsmith64", "password")
        self.assertEqual(actual, expected)

    def test_update_teacher_failed(self):
        expected = False
        actual = teacher.update_teacher(
            1, "John", "Smith", "fm456", "password")
        self.assertEqual(actual, expected)

    def test_delete_teacher(self):
        query = """
        SELECT COUNT(*) FROM teachers;
        """
        pre_deletion_count = postgres_utils.exec_get_all(query)[0][0]
        teacher.delete_teacher(3, 'password')
        post_deletion_count = postgres_utils.exec_get_all(query)[0][0]
        self.assertEqual(pre_deletion_count, (post_deletion_count + 1))

    def test_get_students(self):
        expected = [(1, 'Lawson', 'Xanthe'), (2, 'Stanton', 'Amie')]
        actual = teacher.get_students(1)
        self.assertEqual(actual, expected)

    def test_get_student(self):
        expected = (4, 'Norman', 'Valentina')
        actual = teacher.get_student(4)
        self.assertEqual(actual, expected)

    def test_create_course(self):
        teacher.create_course("Statistics", '', 3)
        query = """
        SELECT * FROM courses
        WHERE id = 6;
        """
        actual = postgres_utils.exec_get_one(query)
        expected = (6, "Statistics", '', 3)
        self.assertEqual(actual, expected)

    def test_get_courses(self):
        actual = teacher.get_courses(3)
        expected = [(4, 'AP US History'), (5, 'Global Studies')]
        self.assertEqual(actual, expected)

    def test_get_course(self):
        expected = (1, 'Algebra I section 01', 'Default course description')
        actual = teacher.get_course(1)
        self.assertEqual(actual, expected)

    def test_update_courses(self):
        teacher.update_course(1, 'AP Calculus AB', '')
        query = """
        SELECT * FROM
        courses
        WHERE id = 1;
        """
        actual = postgres_utils.exec_get_one(query)
        expected = (1, 'AP Calculus AB', '', 1)
        self.assertEqual(actual, expected)

    def test_delete_course(self):
        query = """
        SELECT COUNT(*) FROM courses;
        """
        pre_deletion_count = postgres_utils.exec_get_all(query)[0][0]
        teacher.delete_course(3)
        post_deletion_count = postgres_utils.exec_get_all(query)[0][0]
        self.assertEqual(pre_deletion_count, (post_deletion_count + 1))

    def test_create_assignment(self):
        teacher.create_assignment(
            "HW#3", "Solve for x in the following equations...", "2023/05/17 10:56:43", 1)
        query = """
        SELECT title, instructions
        FROM assignments
        WHERE id = 6;
        """
        expected = ("HW#3", "Solve for x in the following equations...")
        actual = postgres_utils.exec_get_one(query)
        self.assertEqual(actual, expected)

    def test_get_assignments(self):
        actual = teacher.get_assignments(5)
        expected = [
            (1, 'Essay #1', '10/19/04 10:23:54'),
            (4, 'HW#5', '10/19/04 10:23:54')
        ]
        self.assertEqual(actual, expected)

    def test_get_assignment(self):
        actual = teacher.get_assignment(2)
        expected = (2, 'HW#1', 'Graph the following equations f(x)=x^2...',
                    '10/19/04 10:23:54')
        self.assertEqual(actual, expected)

    def test_update_assignment(self):
        teacher.update_assignment(
            1, 'Essay #2', 'Write an essay on the French Revolution and explain...', '2004-10-19 10:23:54')
        query = """
        SELECT title, instructions, due
        FROM assignments
        WHERE id = 1;
        """
        expected = (
            'Essay #2', 'Write an essay on the French Revolution and explain...', datetime.datetime(2004, 10, 19, 10, 23, 54))
        actual = postgres_utils.exec_get_one(query)
        self.assertEqual(actual, expected)

    def test_delete_assignment(self):
        query = """
        SELECT COUNT(*) FROM assignments;
        """
        pre_deletion_count = postgres_utils.exec_get_all(query)[0][0]
        teacher.delete_assignment(3)
        post_deletion_count = postgres_utils.exec_get_all(query)[0][0]
        self.assertEqual(pre_deletion_count, (post_deletion_count + 1))

    def test_get_submissions(self):
        expected = [
            (1, 'Essay #1', 'Lawson', 'Xanthe',
             datetime.datetime(2004, 10, 19, 10, 23, 54)),
            (2, 'Essay #1', 'Norman', 'Valentina',
             datetime.datetime(2004, 10, 19, 10, 23, 54)),
            (3, 'Essay #1', 'Stanton', 'Amie',
             datetime.datetime(2004, 10, 19, 10, 23, 54))
        ]
        actual = teacher.get_submissions(1)
        self.assertEqual(actual, expected)

    def test_get_submission(self):
        expected = (1, 'Essay #1', 'Lorem ipsum...', 'Lawson',
                    'Xanthe', datetime.datetime(2004, 10, 19, 10, 23, 54))
        actual = teacher.get_submission(1)
        self.assertEqual(actual, expected)

    def test_create_grade_successfully(self):
        expected = True
        actual = teacher.create_grade("HW#5", 100, 1)
        self.assertEqual(actual, expected)

    def test_create_grade_failed(self):
        expected = False
        actual = teacher.create_grade("HW#1", 100, 1)
        self.assertEqual(actual, expected)

    def test_create_grade_scores_created(self):
        teacher.create_grade("HW#5", 100, 1)
        conn = postgres_utils.connect()
        cur = conn.cursor()
        query = """
        SELECT *
        FROM scores
        WHERE grade_id = 5;
        """
        cur.execute(query)
        expected = [
            (13, None, '', 5, 1),
            (14, None, '', 5, 3)
        ]
        actual = cur.fetchall()
        self.assertEqual(actual, expected)

    def test_get_all_grades_avg(self):
        expected = [
            (4,
             'HW#4',
             96.67,
             '10/25/04 10:23:54'),
            (3,
             'HW#3',
             80.33,
             '10/23/04 10:23:54'),
            (2,
             'HW#2',
             58.33,
             '10/21/04 10:23:54'),
            (1,
             'HW#1',
             60,
             '10/19/04 10:23:54')
        ]
        actual = teacher.get_all_grades_avg(1)
        self.assertEqual(actual, expected)

    def test_update_grade(self):
        teacher.update_grade(1, "Extra Credit", 70)
        conn = postgres_utils.connect()
        cur = conn.cursor()
        query = """
        SELECT * FROM grades
        WHERE id = 1;
        """
        cur.execute(query)
        expected = (1,
                    'Extra Credit',
                    Decimal('70'),
                    datetime.datetime(2004, 10, 19, 10, 23, 54),
                    1)
        actual = cur.fetchone()
        self.assertEqual(actual, expected)

    def test_delete_grade(self):
        query = """
        SELECT COUNT(*) FROM grades;
        """
        pre_deletion_count = postgres_utils.exec_get_all(query)[0][0]
        teacher.delete_grade(1)
        post_deletion_count = postgres_utils.exec_get_all(query)[0][0]
        self.assertEqual(pre_deletion_count, (post_deletion_count + 1))

    def test_get_scores(self):
        expected = [
            (1, 'HW#1', 50, 'Lawson', 'Xanthe'),
            (2, 'HW#1', 70, 'Norman', 'Valentina'),
            (3, 'HW#1', None, 'Stanton', 'Amie')
        ]
        actual = teacher.get_scores(1)
        self.assertEqual(actual, expected)

    def test_get_score(self):
        expected = ('HW#3', Decimal('66'), Decimal(
            '100'), '', 'Norman', 'Valentina')
        actual = teacher.get_score(8)
        self.assertEqual(actual, expected)

    def test_update_score(self):
        teacher.update_score(4, 50, 'great work!')
        conn = postgres_utils.connect()
        cur = conn.cursor()
        query = """
        SELECT * FROM scores
        WHERE id = 4;
        """
        cur.execute(query)
        expected = (4, Decimal('50'), 'great work!', 2, 1)
        actual = cur.fetchone()
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
