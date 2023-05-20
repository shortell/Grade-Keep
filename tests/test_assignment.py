import datetime
import unittest
from database.db_utils import initialize_database, seed_database
from database.postgres_utils import exec_get_all
from database.assignment import *


class Test_Assignment(unittest.TestCase):

    def setUp(self):
        initialize_database()
        seed_database()

    def test_create_assignment(self):
        create_assignment(
            "HW#3", "Solve for x in the following equations...", "2023/05/17 10:56:43", 1)
        query = """
        SELECT title, instructions
        FROM assignments
        WHERE id = 6;
        """
        expected = ("HW#3", "Solve for x in the following equations...")
        actual = exec_get_one(query)
        self.assertEqual(actual, expected)

    def test_get_assignments(self):
        actual = get_assignments(5)
        expected = [
            (1, 'Essay #1', datetime.datetime(2004, 10, 19, 10, 23, 54)),
            (4, 'HW#5', datetime.datetime(2004, 10, 19, 10, 23, 54))
        ]
        self.assertEqual(actual, expected)

    def test_get_assignment(self):
        actual = get_assignment(2)
        expected = (2, 'HW#1', 'Graph the following equations f(x)=x^2...',
                    datetime.datetime(2004, 10, 19, 10, 23, 54))
        self.assertEqual(actual, expected)

    def test_update_assignment(self):
        update_assignment(
            1, 'Essay #2', 'Write an essay on the French Revolution and explain...', '2004-10-19 10:23:54')
        query = """
        SELECT title, instructions, due
        FROM assignments
        WHERE id = 1;
        """
        expected = (
            'Essay #2', 'Write an essay on the French Revolution and explain...', datetime.datetime(2004, 10, 19, 10, 23, 54))
        actual = exec_get_one(query)
        self.assertEqual(actual, expected)

    def test_delete_assignment(self):
        query = """
        SELECT COUNT(*) FROM assignments;
        """
        pre_deletion_count = exec_get_all(query)[0][0]
        delete_assignment(3)
        post_deletion_count = exec_get_all(query)[0][0]
        self.assertEqual(pre_deletion_count, (post_deletion_count + 1))
