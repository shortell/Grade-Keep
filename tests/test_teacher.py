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
        expected = [(1, 'Sidney', 'Velazquez'), ]
        self.assertEqual(actual, expected)

    def test_get_teacher_failed(self):
        actual = get_teacher('sv124', 'password1')
        expected = []
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
