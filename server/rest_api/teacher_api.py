from flask import session
from flask_restful import Resource, request, abort
from db import teacher
from rest_api import rest_utils


import sys




def is_logged_in():
    return session.get("id") is not None


def is_teacher():
    return session.get("account_type") == "teacher"


def is_course_authorized(course_id):
    if course_id in session["course_ids"]:
        return True
    abort(403, message="you are not authorized to access this course")


def is_assignment_authorized(course_id, assignment_id):
    if assignment_id in session["assignment_ids"]:
        return is_course_authorized(course_id)
    abort(403, message="you are not authorized to access this assignment")


def is_enrollment_authorized(course_id, enrollment_id):
    if enrollment_id in session["enrollment_ids"]:
        return is_course_authorized(course_id)
    abort(403, message="you are not authorized to access this students enrollment")


def is_submission_authorized(course_id, assignment_id, submission_id):
    if submission_id in session["submission_ids"]:
        return is_assignment_authorized(course_id, assignment_id)
    abort(403, message="you are not authorized to access this submission")


def is_grade_authorized(course_id, grade_id):
    if grade_id in session["grade_ids"]:
        return is_course_authorized(course_id)
    abort(403, message="you are not authorized to access this grade")


def is_score_authorized(course_id, grade_id, score_id):
    if score_id in session["score_ids"]:
        return is_grade_authorized(course_id, grade_id)
    abort(403, message="you are not authorized to access this score")


class Teachers(Resource):
    def get(self):
        if rest_utils.is_session_valid(session["account_type"]):
            id = session["id"]
            return teacher.get_teacher(id)

    def put(self):
        if rest_utils.is_session_valid(session["account_type"]):
            id = session["id"]
            username = request.form['username']
            password = request.form['password']
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            return teacher.update_teacher(id, first_name, last_name, username, password)

    def delete(self):
        if rest_utils.is_session_valid(session["account_type"]):
            id = session["id"]
            password = request.form['password']
            teacher.delete_teacher(id, password)
            return 200


class Courses(Resource):
    def post(self):
        if rest_utils.is_session_valid(session["account_type"]):
            title = request.form['title']
            description = request.form['description']
            id = session["id"]
            teacher.create_course(title, description, id)
            return 201

    def get(self):
        if rest_utils.is_session_valid(session["account_type"]):
            session_id = session["id"]
            courses = teacher.get_courses(session_id)
            course_ids = [record[0]
                          for record in courses] if courses is not None else []
            session["course_ids"] = course_ids
            return courses


class Course(Resource):
    def get(self, course_id):
        if rest_utils.is_session_valid(session["account_type"]) and is_course_authorized(course_id):
            return list(teacher.get_course(course_id))

    def put(self, course_id):
        if rest_utils.is_session_valid(session["account_type"]) and is_course_authorized(course_id):
            title = request.form['title']
            description = request.form['description']
            teacher.update_course(course_id, title, description)
            return 200

    def delete(self, course_id):
        if rest_utils.is_session_valid(session["account_type"]) and is_course_authorized(course_id):
            teacher.delete_course(course_id)
            return 200


class Students(Resource):
    def get(self, course_id):
        if rest_utils.is_session_valid(session["account_type"]) and is_course_authorized(course_id):
            students = teacher.get_students(course_id)
            enrollment_ids = [record[0]
                              for record in students] if students is not None else []
            session["enrollment_ids"] = enrollment_ids
            return students


class Student(Resource):
    def get(self, course_id, enrollment_id):
        if rest_utils.is_session_valid(session["account_type"]) and is_enrollment_authorized(course_id, enrollment_id):
            return teacher.get_student(enrollment_id)


class Assignments(Resource):
    def post(self, course_id):
        if rest_utils.is_session_valid(session["account_type"]) and is_course_authorized(course_id):
            title = request.form['title']
            instructions = request.form['instructions']
            due = request.form['due']
            teacher.create_assignment(title, instructions, due, course_id)
            return 201

    def get(self, course_id):
        if rest_utils.is_session_valid(session["account_type"]) and is_course_authorized(course_id):
            assignments = teacher.get_assignments(course_id)
            assignment_ids = [record[0]
                              for record in assignments] if assignments is not None else []
            session["assignment_ids"] = assignment_ids
            return assignments


class Assignment(Resource):
    def get(self, course_id, assignment_id):
        if rest_utils.is_session_valid(session["account_type"]) and is_assignment_authorized(course_id, assignment_id):
            return teacher.get_assignment(assignment_id)

    def put(self, course_id, assignment_id):
        if rest_utils.is_session_valid(session["account_type"]) and is_assignment_authorized(course_id, assignment_id):
            title = request.form['title']
            instructions = request.form['instructions']
            due = request.form['due']
            teacher.update_assignment(assignment_id, title, instructions, due)
            return 200

    def delete(self, course_id, assignment_id):
        if rest_utils.is_session_valid(session["account_type"]) and is_assignment_authorized(course_id, assignment_id):
            teacher.delete_assignment(assignment_id)
            return 200


class Submissions(Resource):
    def get(self, course_id, assignment_id):
        if rest_utils.is_session_valid(session["account_type"]) and is_assignment_authorized(course_id, assignment_id):
            submissions = teacher.get_submissions(assignment_id)
            submission_ids = [record[0]
                              for record in submissions] if submissions is not None else []
            session["submission_ids"] = submission_ids
            return submissions


class Submission(Resource):
    def get(self, course_id, assignment_id, submission_id):
        if rest_utils.is_session_valid(session["account_type"]) and is_submission_authorized(course_id, assignment_id, submission_id):
            return teacher.get_submission(submission_id)


class Grades(Resource):
    def post(self, course_id):
        if rest_utils.is_session_valid(session["account_type"]) and is_course_authorized(course_id):
            title = request.form['title']
            total_points = request.form['total_points']
            teacher.create_grade(title, total_points, course_id)
            return 201

    def get(self, course_id):
        if rest_utils.is_session_valid(session["account_type"]) and is_course_authorized(course_id):
            grades = teacher.get_all_grades_avg(course_id)
            grade_ids = [record[0]
                         for record in grades] if grades is not None else []
            session["grade_ids"] = grade_ids
            return grades


class Grade(Resource):
    def put(self, course_id, grade_id):
        if rest_utils.is_session_valid(session["account_type"]) and is_grade_authorized(course_id, grade_id):
            title = request.form['title']
            total_points = request.form['total_points']
            teacher.update_grade(grade_id, title, total_points)
            return 200

    def delete(self, course_id, grade_id):
        if rest_utils.is_session_valid(session["account_type"]) and is_grade_authorized(course_id, grade_id):
            teacher.delete_grade(grade_id)
            return 200


class Scores(Resource):
    def get(self, course_id, grade_id):
        if rest_utils.is_session_valid(session["account_type"]) and is_grade_authorized(course_id, grade_id):
            scores = teacher.get_scores(grade_id)
            score_ids = [record[0]
                         for record in scores] if scores is not None else []
            session["score_ids"] = score_ids
            return scores


class Score(Resource):
    def get(self, course_id, grade_id, score_id):
        if rest_utils.is_session_valid(session["account_type"]) and is_score_authorized(course_id, grade_id, score_id):
            return teacher.get_score(score_id)

    def put(self, course_id, grade_id, score_id):
        if rest_utils.is_session_valid(session["account_type"]) and is_score_authorized(course_id, grade_id, score_id):
            points_earned = request.form['points_earned']
            comments = request.form['comments']
            teacher.update_score(score_id, points_earned, comments)
