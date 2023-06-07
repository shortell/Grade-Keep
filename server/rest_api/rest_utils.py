from flask import session, make_response
from flask_restful import abort

def create_response(data, status_code):
    response = make_response(data)
    response.status_code = status_code
    return response

def is_logged_in():
    return session.get("id") is not None


def is_role(role):
    return session.get("account_type") == role


def is_session_valid(role):
    if not is_logged_in():
        abort(401, message="you must log in to make this request")
    if not is_role(role):
        abort(403, message="you must be a {} to make this request".format(role))
    return True


def is_course_authorized(course_id):
    if course_id in session["course_ids"]:
        return True
    abort(403, message="you are not authorized to access this course")


def is_assignment_authorized(course_id, assignment_id):
    if assignment_id in session["assignment_ids"]:
        return is_course_authorized(course_id)
    abort(403, message="you are not authorized to access this assignment")


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
