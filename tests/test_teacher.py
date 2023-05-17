import unittest
from database.db_utils import initialize_database, seed_database
from database.postgres_utils import *
from database.teacher import *


class Test_Teacher(unittest.TestCase):

    def setUp(self):
        initialize_database()
        seed_database()

    # testing teacher related functions

    def test_create_teacher_successfully(self):
        actual = create_teacher("johnSmith123", "password")
        expected = True
        self.assertEqual(actual, expected)

    def test_create_teacher_failed(self):
        actual = create_teacher("sv123", "password")
        expected = False
        self.assertEqual(actual, expected)

    def test_get_teacher_successfully(self):
        actual = get_teacher('sv123', 'password')
        expected = (1, 'Sidney', 'Velazquez')
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

    # testing teachers control over classes

    def test_create_class(self):
        create_class("Statistics", 3)
        query = """
        SELECT * FROM classes
        WHERE id = 6;
        """
        actual = exec_get_one(query)
        expected = (6, "Statistics", 3)
        self.assertEqual(actual, expected)

    def test_get_classes(self):
        actual = get_classes(3)
        expected = [(4, 'AP US History'), (5, 'Global Studies')]
        self.assertEqual(actual, expected)

    def test_update_classes(self):
        update_class(1, 'AP Calculus AB')
        query = """
        SELECT * FROM
        classes
        WHERE id = 1;
        """
        actual = exec_get_one(query)
        expected = (1, 'AP Calculus AB', 1)
        self.assertEqual(actual, expected)

    def test_delete_class(self):
        query = """
        SELECT COUNT(*) FROM classes;
        """
        pre_deletion_count = exec_get_all(query)[0][0]
        delete_class(3)
        post_deletion_count = exec_get_all(query)[0][0]
        self.assertEqual(pre_deletion_count, (post_deletion_count + 1))

    # test teachers control over assignments

    def test_create_assignment(self):
        create_assignment(
            "HW#3", "Solve for x in the following equations...", 1)
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
            (1, 'Essay #1'),
            (4, 'HW#5')
        ]
        self.assertEqual(actual, expected)

    def test_get_assignment(self):
        actual = get_assignment(2)
        expected = (2, 'HW#1', 'Graph the following equations f(x)=x^2...')
        self.assertEqual(actual, expected)

    def test_update_assignment(self):
        update_assignment(
            1, 'Essay #2', 'Write an essay on the French Revolution and explain...')
        query = """
        SELECT title, instructions
        FROM assignments
        WHERE id = 1;
        """
        expected = (
            'Essay #2', 'Write an essay on the French Revolution and explain...')
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

    # test teachers control over submissions

    def test_get_submissions(self):
        expected = [
            (1, 'Essay #1', 'Lawson', 'Xanthe'),
            (2, 'Essay #1', 'Norman', 'Valentina'),
            (3, 'Essay #1', 'Stanton', 'Amie')
        ]
        actual = get_submissions(1)
        self.assertEqual(actual, expected)

    def test_get_submission(self):
        expected = (1, 'Essay #1', 'Lorem ipsum...', 'Lawson', 'Xanthe')
        actual = get_submission(1)
        self.assertEqual(actual, expected)

    # test teachers ability to grade and view students

    def test_get_students(self):
        expected = [(1, 'Lawson', 'Xanthe'), (2, 'Stanton', 'Amie')]
        actual = get_students(1)
        self.assertEqual(actual, expected)

    def test_get_student(self):
        expected = (4, 'Norman', 'Valentina')
        actual = get_student(4)
        self.assertEqual(actual, expected)

    # test teachers ability to control grades

    def test_create_grade_with_earned_points(self):
        create_grade("HW#1", 10, 1, 9)
        query = """
        SELECT title, points_earned, total_points FROM grades
        WHERE id = 5;
        """
        expected = ("HW#1", 9, 10)
        actual = exec_get_one(query)
        self.assertEqual(actual, expected)

    def test_create_grade_with_out_earned_points(self):
        create_grade("HW#1", 10, 1)
        query = """
        SELECT title, points_earned, total_points FROM grades
        WHERE id = 5;
        """
        expected = ("HW#1", None, 10)
        actual = exec_get_one(query)
        self.assertEqual(actual, expected)

    def test_get_grades(self):
        expected = [
            (1, 'HW#1', None),
            (2, 'HW#2', 100.0),
            (3, 'HW#3', 50.0),
            (4, 'HW#4', 30.0)
        ]
        actual = get_grades(1)
        self.assertEqual(actual, expected)

    def test_get_grade_with_null_earned_points(self):
        expected = (1, 'HW#1', None, 100.0)
        actual = get_grade(1)
        self.assertEqual(actual, expected)

    def test_get_grade_with_earned_points(self):
        expected = (3, 'HW#3', 50.0, 100.0)
        actual = get_grade(3)
        self.assertEqual(actual, expected)
