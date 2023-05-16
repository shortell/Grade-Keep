import unittest
from database.db_utils import *

class Test_db_utils(unittest.TestCase):

    def test_initialize_database(self):
        initialize_database()