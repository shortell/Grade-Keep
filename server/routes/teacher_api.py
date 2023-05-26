from flask import session
from flask_restful import Resource, request
from db import teacher

def is_logged_in():
    return session.get("id") is not None

def is_session_valid():
    return session["account_type"] == "teacher" and session.get("id") is not None

class Teacher(Resource):
    def get(self):
        # if is_logged_in():
        id = session["id"]
        return teacher.get_courses(id)
        # return 401
    
    def put(self):
        id = session["id"]
        username = request.form['username']
        password = request.form['password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        return teacher.update_teacher(id, first_name, last_name, username, password)
    
    def delete(self):
        id = session["id"]
        password = request.form['password']
        teacher.delete_teacher(id, password)
        return 200