import unittest
from database.db_utils import initialize_database
from database.postgres_utils import exec_get_all
from database.teacher import *


class Test_Teacher(unittest.TestCase):

    def setUp(self):
        initialize_database()

    def test_register(self):
        register("johnSmith123", "password")
        query = """
        SELECT * FROM teachers;
        """
        expected = [(1, '', '', 'johnSmith123', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8'), ]
        actual = exec_get_all(query)
        self.assertEqual(actual, expected)
