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
