import unittest
from database.postgres_utils import connect
from database.db_utils import initialize_database, seed_database
from database.teacher import *


class Test_Grade(unittest.TestCase):

    def setUp(self):
        initialize_database()
        seed_database()

    def test_create_grade(self):
        create_grade("test", 100, 1)
        create_grade("test", 100, 2)
        create_grade("test2", 100, 1)
        create_grade("test", 100, 1)