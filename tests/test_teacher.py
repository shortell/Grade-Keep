import unittest
from database.db_utils import initialize_database, seed_database
from database.postgres_utils import exec_get_all
from database.teacher import *


class Test_Teacher(unittest.TestCase):

    def setUp(self):
        initialize_database()
        seed_database()

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

    # # test teachers control over assignments

    # # test teachers control over submissions

   

    # # test teachers ability to grade and view students

    # def test_get_students(self):
    #     expected = [(1, 'Lawson', 'Xanthe'), (2, 'Stanton', 'Amie')]
    #     actual = get_students(1)
    #     self.assertEqual(actual, expected)

    # def test_get_student(self):
    #     expected = (4, 'Norman', 'Valentina')
    #     actual = get_student(4)
    #     self.assertEqual(actual, expected)

    # # test teachers ability to control grades

    # def test_create_grade_with_earned_points(self):
    #     create_grade("HW#1", 10, 1, 9)
    #     query = """
    #     SELECT title, points_earned, total_points FROM grades
    #     WHERE id = 5;
    #     """
    #     expected = ("HW#1", 9, 10)
    #     actual = exec_get_one(query)
    #     self.assertEqual(actual, expected)

    # def test_create_grade_with_out_earned_points(self):
    #     create_grade("HW#1", 10, 1)
    #     query = """
    #     SELECT title, points_earned, total_points FROM grades
    #     WHERE id = 5;
    #     """
    #     expected = ("HW#1", None, 10)
    #     actual = exec_get_one(query)
    #     self.assertEqual(actual, expected)
