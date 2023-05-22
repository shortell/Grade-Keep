from decimal import Decimal
import unittest
import datetime
from database.db_utils import initialize_database, seed_database
from database.postgres_utils import exec_get_all
from database.teacher import *


class Test_Teacher(unittest.TestCase):

    def setUp(self):
        initialize_database()
        seed_database()

    def test_create_teacher_successfully(self):
        actual = create_teacher("John", "Smith", "johnSmith123", "password")
        expected = True
        self.assertEqual(actual, expected)

    def test_create_teacher_failed(self):
        actual = create_teacher("Sidney", "Velazquez", "sv123", "password")
        expected = False
        self.assertEqual(actual, expected)

    def test_get_teacher_successfully(self):
        actual = get_teacher('sv123', 'password')
        expected = (1, 'Sidney', 'Velazquez', 'sv123')
        self.assertEqual(actual, expected)

    def test_get_teacher_failed(self):
        actual = get_teacher('sv124', 'password1')
        expected = None
        self.assertEqual(actual, expected)

    def test_update_teacher(self):
        update_teacher(1, "John", "Smith")
        query = """
        SELECT id, first_name, last_name FROM teachers
        WHERE id = 1;
        """
        expected = [(1, "John", "Smith"), ]
        actual = exec_get_all(query)
        self.assertEqual(actual, expected)

    def test_delete_teacher(self):
        query = """
        SELECT COUNT(*) FROM teachers;
        """
        pre_deletion_count = exec_get_all(query)[0][0]
        delete_teacher(3, 'password')
        post_deletion_count = exec_get_all(query)[0][0]
        self.assertEqual(pre_deletion_count, (post_deletion_count + 1))

    def test_get_students(self):
        expected = [(1, 'Lawson', 'Xanthe'), (2, 'Stanton', 'Amie')]
        actual = get_students(1)
        self.assertEqual(actual, expected)

    def test_get_student(self):
        expected = (4, 'Norman', 'Valentina')
        actual = get_student(4)
        self.assertEqual(actual, expected)

    def test_create_course(self):
        create_course("Statistics", 3)
        query = """
        SELECT * FROM courses
        WHERE id = 6;
        """
        actual = exec_get_one(query)
        expected = (6, "Statistics", '', 3)
        self.assertEqual(actual, expected)

    def test_get_courses(self):
        actual = get_courses(3)
        expected = [(4, 'AP US History'), (5, 'Global Studies')]
        self.assertEqual(actual, expected)

    def test_update_courses(self):
        update_course(1, 'AP Calculus AB')
        query = """
        SELECT * FROM
        courses
        WHERE id = 1;
        """
        actual = exec_get_one(query)
        expected = (1, 'AP Calculus AB', '', 1)
        self.assertEqual(actual, expected)

    def test_delete_course(self):
        query = """
        SELECT COUNT(*) FROM courses;
        """
        pre_deletion_count = exec_get_all(query)[0][0]
        delete_course(3)
        post_deletion_count = exec_get_all(query)[0][0]
        self.assertEqual(pre_deletion_count, (post_deletion_count + 1))

    def test_create_assignment(self):
        create_assignment(
            "HW#3", "Solve for x in the following equations...", "2023/05/17 10:56:43", 1)
        query = """
        SELECT title, instructions
        FROM assignments
        WHERE id = 6;
        """
        expected = ("HW#3", "Solve for x in the following equations...")
        actual = exec_get_one(query)
        self.assertEqual(actual, expected)

    def test_get_assignments(self):
        actual = get_assignments(5)
        expected = [
            (1, 'Essay #1', datetime.datetime(2004, 10, 19, 10, 23, 54)),
            (4, 'HW#5', datetime.datetime(2004, 10, 19, 10, 23, 54))
        ]
        self.assertEqual(actual, expected)

    def test_get_assignment(self):
        actual = get_assignment(2)
        expected = (2, 'HW#1', 'Graph the following equations f(x)=x^2...',
                    datetime.datetime(2004, 10, 19, 10, 23, 54))
        self.assertEqual(actual, expected)

    def test_update_assignment(self):
        update_assignment(
            1, 'Essay #2', 'Write an essay on the French Revolution and explain...', '2004-10-19 10:23:54')
        query = """
        SELECT title, instructions, due
        FROM assignments
        WHERE id = 1;
        """
        expected = (
            'Essay #2', 'Write an essay on the French Revolution and explain...', datetime.datetime(2004, 10, 19, 10, 23, 54))
        actual = exec_get_one(query)
        self.assertEqual(actual, expected)

    def test_delete_assignment(self):
        query = """
        SELECT COUNT(*) FROM assignments;
        """
        pre_deletion_count = exec_get_all(query)[0][0]
        delete_assignment(3)
        post_deletion_count = exec_get_all(query)[0][0]
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
        actual = get_submissions(1)
        self.assertEqual(actual, expected)

    def test_get_submission(self):
        expected = (1, 'Essay #1', 'Lorem ipsum...', 'Lawson',
                    'Xanthe', datetime.datetime(2004, 10, 19, 10, 23, 54))
        actual = get_submission(1)
        self.assertEqual(actual, expected)

    def test_create_grade_successfully(self):
        expected = True
        actual = create_grade("HW#5", 100, 1)
        self.assertEqual(actual, expected)

    def test_create_grade_failed(self):
        expected = False
        actual = create_grade("HW#1", 100, 1)
        self.assertEqual(actual, expected)

    def test_create_grade_scores_created(self):
        create_grade("HW#5", 100, 1)
        conn = connect()
        cur = conn.cursor()
        query = """
        SELECT *
        FROM scores
        WHERE grade_id = 5;
        """
        cur.execute(query)
        expected = [
            (13, None, 5, 1),
            (14, None, 5, 3)
        ]
        actual = cur.fetchall()
        self.assertEqual(actual, expected)

    def test_get_grades(self):
        expected = [(1,
                     'HW#1',
                     Decimal('0.46666666666666666667'),
                     datetime.datetime(2004, 10, 19, 10, 23, 54)),
                    (2,
                     'HW#2',
                     Decimal('0.58333333333333333333'),
                     datetime.datetime(2004, 10, 19, 10, 23, 54)),
                    (3,
                     'HW#3',
                     Decimal('0.80333333333333333333'),
                     datetime.datetime(2004, 10, 19, 10, 23, 54)),
                    (4,
                     'HW#4',
                     Decimal('0.96666666666666666667'),
                     datetime.datetime(2004, 10, 19, 10, 23, 54))
                    ]
        actual = get_grades(1)
        self.assertEqual(actual, expected)

    def test_update_grade(self):
        update_grade(1, "Extra Credit", 70)
        conn = connect()
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
        pre_deletion_count = exec_get_all(query)[0][0]
        delete_grade(1)
        post_deletion_count = exec_get_all(query)[0][0]
        self.assertEqual(pre_deletion_count, (post_deletion_count + 1))

    def test_get_scores(self):
        expected = [
            (1, 'HW#1', Decimal('0.50000000000000000000'), 'Lawson', 'Xanthe'),
            (2, 'HW#1', Decimal('0.70000000000000000000'), 'Norman', 'Valentina'),
            (3, 'HW#1', Decimal('0.20000000000000000000'), 'Stanton', 'Amie')
        ]
        actual = get_scores(1)
        self.assertEqual(actual, expected)

    def test_get_score(self):
        expected = ('HW#3', Decimal('66'), Decimal(
            '100'), 'Norman', 'Valentina')
        actual = get_score(8)
        self.assertEqual(actual, expected)

    def test_update_score(self):
        update_score(4, 50)
        conn = connect()
        cur = conn.cursor()
        query = """
        SELECT * FROM scores
        WHERE id = 4;
        """
        cur.execute(query)
        expected = (4, Decimal('50'), 2, 1)
        actual = cur.fetchone()
        self.assertEqual(actual, expected)
