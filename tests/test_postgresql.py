import unittest
from server.database.postgres_utils import exec_get_one


class TestPostgreSQL(unittest.TestCase):

    def test_can_connect(self):
        result = exec_get_one('SELECT VERSION()')
        self.assertTrue(result[0].startswith('PostgreSQL'))


if __name__ == '__main__':
    unittest.main()
