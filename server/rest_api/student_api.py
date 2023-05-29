from flask import session
from flask_restful import Resource, request, abort
from db import student
import rest_utils


class Students(Resource):
    def get(self):
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
