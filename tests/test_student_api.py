import unittest
from tests.test_utils import get_rest_call, post_rest_call
from server.db import db_utils


class TestAuthAPI(unittest.TestCase):

    def setUp(self):
        db_utils.initialize_database()
        db_utils.seed_database()

    def test_students_get(self):
        data = {"account_type": "student",
                "username": "xl123", "password": "password"}
        post_response = post_rest_call("http://127.0.0.1:5000/login", data)
        get_response = get_rest_call("http://127.0.0.1:5000/student")
        print(post_response.content)
        print(get_response.content)


if __name__ == '__main__':
    unittest.main()