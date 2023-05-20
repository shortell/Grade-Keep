import unittest, datetime
from database.db_utils import initialize_database, seed_database
from database.postgres_utils import *
from database.submission import *


class Test_Submission(unittest.TestCase):

    def setUp(self):
        initialize_database()
        seed_database()

    def test_get_submissions(self):
        expected = [
            (1, 'Essay #1', 'Lawson', 'Xanthe', datetime.datetime(2004, 10, 19, 10, 23, 54)),
            (2, 'Essay #1', 'Norman', 'Valentina', datetime.datetime(2004, 10, 19, 10, 23, 54)),
            (3, 'Essay #1', 'Stanton', 'Amie', datetime.datetime(2004, 10, 19, 10, 23, 54))
        ]
        actual = get_submissions(1)
        self.assertEqual(actual, expected)

    def test_get_submission(self):
        expected = (1, 'Essay #1', 'Lorem ipsum...', 'Lawson', 'Xanthe', datetime.datetime(2004, 10, 19, 10, 23, 54))
        actual = get_submission(1)
        self.assertEqual(actual, expected)
