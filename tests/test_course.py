import unittest
from database.db_utils import initialize_database, seed_database
from database.postgres_utils import *
from database.course import *


class Test_Course(unittest.TestCase):

    def setUp(self):
        initialize_database()
        seed_database()

    def test_create_course(self):
        create_course("Statistics", 3)
        query = """
        SELECT * FROM courses
        WHERE id = 6;
        """
        actual = exec_get_one(query)
        expected = (6, "Statistics", 3)
        self.assertEqual(actual, expected)

    def test_get_teachers_courses(self):
        actual = get_teachers_courses(3)
        expected = [(4, 'AP US History'), (5, 'Global Studies')]
        self.assertEqual(actual, expected)

    def test_get_students_courses(self):
        actual = get_students_courses(3)
        expected = [(1, 'Algebra I section 01')]
        self.assertEqual(actual, expected)

    def test_update_courses(self):
        update_course(1, 'AP Calculus AB')
        query = """
        SELECT * FROM
        courses
        WHERE id = 1;
        """
        actual = exec_get_one(query)
        expected = (1, 'AP Calculus AB', 1)
        self.assertEqual(actual, expected)

    def test_delete_course(self):
        query = """
        SELECT COUNT(*) FROM courses;
        """
        pre_deletion_count = exec_get_all(query)[0][0]
        delete_course(3)
        post_deletion_count = exec_get_all(query)[0][0]
        self.assertEqual(pre_deletion_count, (post_deletion_count + 1))
