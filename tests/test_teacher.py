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

    def test_delete_teacher(self):
        query = """
        SELECT COUNT(*) FROM classes;
        """
        pre_deletion_count = exec_get_all(query)[0][0]
        delete_class(3)
        post_deletion_count = exec_get_all(query)[0][0]
        self.assertEqual(pre_deletion_count, (post_deletion_count + 1))
