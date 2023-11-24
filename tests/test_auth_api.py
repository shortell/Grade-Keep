# import unittest
# from tests.test_utils import get_rest_call, post_rest_call
# from server.db import db_utils


# class TestAuthAPI(unittest.TestCase):

#     def setUp(self):
#         db_utils.initialize_database()
#         db_utils.seed_database()

#     def test_login_get(self):
#         actual = get_rest_call("http://127.0.0.1:5000/login")
#         expected = 200
#         self.assertEqual(actual, expected)

#     def test_login_post_succeed(self):
#         data = {"account_type": "teacher",
#                 "username": "sv123", "password": "password"}
#         actual = post_rest_call("http://127.0.0.1:5000/login", data)
#         expected = 200
#         self.assertEqual(actual, expected)

#     def test_login_post_fail(self):
#         data = {"account_type": "teacher",
#                 "username": "john", "password": "password"}
#         actual = post_rest_call("http://127.0.0.1:5000/login", data)
#         expected = 400
#         self.assertEqual(actual, expected)

#     def test_logout_get(self):
#         actual = get_rest_call("http://127.0.0.1:5000/logout")
#         expected = 200
#         self.assertEqual(actual, expected)

#     def test_register_get(self):
#         actual = get_rest_call("http://127.0.0.1:5000/register")
#         expected = 200
#         self.assertEqual(actual, expected)

#     def test_register_post_succeed(self):
#         data = {"account_type": "teacher", "username": "js123",
#                 "password": "password", "first_name": "john", "last_name": "smith"}
#         actual = post_rest_call("http://127.0.0.1:5000/register", data)
#         expected = 201
#         self.assertEqual(actual, expected)

#     def test_register_post_fail_1(self):
#         data = {"account_type": "admin", "username": "js123",
#                 "password": "password", "first_name": "john", "last_name": "smith"}
#         actual = post_rest_call("http://127.0.0.1:5000/register", data)
#         expected = 400
#         self.assertEqual(actual, expected)

#     def test_register_post_fail_2(self):
#         data = {"account_type": "teacher", "username": "sv123",
#                 "password": "password", "first_name": "john", "last_name": "smith"}
#         actual = post_rest_call("http://127.0.0.1:5000/register", data)
#         expected = 400
#         self.assertEqual(actual, expected)


# if __name__ == '__main__':
#     unittest.main()
