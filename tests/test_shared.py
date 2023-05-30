import unittest
from server.db import shared, db_utils


class Test_Teacher(unittest.TestCase):

    def setUp(self):
        db_utils.initialize_database()
        db_utils.seed_database()

    def test_get_assignments(self):
        actual = shared.get_assignments(5)
        expected = [
            (1, 'Essay #1', '10/19/04 10:23:54'),
            (4, 'HW#5', '10/19/04 10:23:54')
        ]
        self.assertEqual(actual, expected)

    def test_get_assignment(self):
        actual = shared.get_assignment(2)
        expected = (2, 'HW#1', 'Graph the following equations f(x)=x^2...',
                    '10/19/04 10:23:54')
        self.assertEqual(actual, expected)
