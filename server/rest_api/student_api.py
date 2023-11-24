from flask import session
from flask_restful import Resource, request
from db import student, shared
from rest_api import rest_utils


class Students(Resource):
    def get(self):
        print(session + " student_api.py")
        if rest_utils.is_session_valid("student"):
            id = session["id"]
            return student.get_student(id)

    def put(self):
        if rest_utils.is_session_valid("student"):
            id = session["id"]
            username = request.form['username']
            password = request.form['password']
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            return student.update_student(id, first_name, last_name, username, password)

    def delete(self):
        if rest_utils.is_session_valid("student"):
            id = session["id"]
            password = request.form['password']
            student.delete_student(id, password)
            return 200


class S_Courses(Resource):
    def get(self):
        if rest_utils.is_session_valid("student"):
            id = session["id"]
            courses = student.get_courses(id)
            course_ids = [record[0]
                          for record in courses] if courses is not None else []
            session["course_ids"] = course_ids
            return courses


class S_Course(Resource):
    def get(self, course_id):
        if rest_utils.is_session_valid("student") and rest_utils.is_course_authorized(course_id):
            return list(student.get_course(course_id))


class S_Assignments(Resource):
    def get(self, course_id):
        if rest_utils.is_session_valid("student") and rest_utils.is_course_authorized(course_id):
            assignments = shared.get_assignments(course_id)
            assignment_ids = [record[0]
                              for record in assignments] if assignments is not None else []
            session["assignment_ids"] = assignment_ids
            return assignments


class S_Assignment(Resource):
    def get(self, course_id, assignment_id):
        if rest_utils.is_session_valid("student") and rest_utils.is_assignment_authorized(course_id, assignment_id):
            return shared.get_assignment(assignment_id)


class S_Submissions(Resource):
    def post(self, course_id, assignment_id):
        if rest_utils.is_session_valid("student") and rest_utils.is_assignment_authorized(course_id, assignment_id):
            response = request.form['response']
            student.create_submission(response, assignment_id, session["id"])
            return 201

    def get(self, course_id, assignment_id):
        if rest_utils.is_session_valid("student") and rest_utils.is_assignment_authorized(course_id, assignment_id):
            id = session["id"]
            submissions = student.get_submission(id, assignment_id)
            submission_ids = [record[0]
                              for record in submissions] if submissions is not None else []
            session["submission_ids"] = submission_ids
            return submissions


class S_Submission(Resource):
    def put(self, course_id, assignment_id, submission_id):
        if rest_utils.is_session_valid("student") and rest_utils.is_submission_authorized(course_id, assignment_id, submission_id):
            response = request.form['response']
            student.update_submission(submission_id, response)
            return 200

    def delete(self, course_id, assignment_id, submission_id):
        if rest_utils.is_session_valid("student") and rest_utils.is_submission_authorized(course_id, assignment_id, submission_id):
            student.delete_submission(submission_id)
            return 200


class S_Grades(Resource):
    def get(self, course_id):
        if rest_utils.is_session_valid("student") and rest_utils.is_course_authorized(course_id):
            course_avg = student.get_score_average_by_course( # to be used
                session["id"], course_id)
            grades = student.get_grades(session["id"], course_id)
            grade_ids = [record[0]
                         for record in grades] if grades is not None else []
            session["grade_ids"] = grade_ids
            return grades


class S_Scores(Resource):
    def get(self, course_id, grade_id):
        if rest_utils.is_session_valid("student") and rest_utils.is_grade_authorized(course_id, grade_id):
            id = session["id"]
            return student.get_score(id, grade_id)
