# import unittest
# from database.db_utils import initialize_database, seed_database
# from database.student import *


# class Test_Student(unittest.TestCase):

#     def setUp(self):
#         initialize_database()
#         seed_database()

#     def test_create_student_successfully(self):
#         actual = create_student("John", "Smith", "johnSmith123", "password")
#         expected = True
#         self.assertEqual(actual, expected)

#     def test_create_student_failed(self):
#         actual = create_student('Xanthe', 'Lawson', 'xl123', "password")
#         expected = False
#         self.assertEqual(actual, expected)

