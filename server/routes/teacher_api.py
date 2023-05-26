from flask import session
from flask_restful import Resource, request, abort
from db import teacher


import sys

sys.path.insert(0, 'c:/Users/jacks/Coding_Projects/Grade-Keep/server/db')


def is_logged_in():
    return session.get("id") is not None


def is_teacher():
    return session.get("account_type") == "teacher"


def is_session_valid():
    if not is_logged_in():
        abort(401, message="you must log in to make this request")

    if not is_teacher():
        abort(403, message="you must be a teacher to make this request")

    return True


class Teacher(Resource):
    def get(self):
        if is_session_valid():
            id = session["id"]
            return teacher.get_courses(id)

    def put(self):
        if is_session_valid():
            id = session["id"]
            username = request.form['username']
            password = request.form['password']
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            return teacher.update_teacher(id, first_name, last_name, username, password)

    def delete(self):
        if is_session_valid():
            id = session["id"]
            password = request.form['password']
            teacher.delete_teacher(id, password)
            return 200
