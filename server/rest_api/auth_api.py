from flask import session
from flask_restful import Resource, request
from db import teacher, student


class Login(Resource):
    def get(self):
        return 200

    def post(self):
        account_type = request.form['account_type']
        username = request.form['username']
        password = request.form['password']

        if account_type in ['teacher', 'student']:
            login_func = teacher.login if account_type == 'teacher' else student.login
            result = login_func(username, password)

            if result is not None:
                session['account_type'] = account_type
                session['id'] = result[0]
                return 200

        return 400


class Logout(Resource):
    def get(self):
        session.clear()
        return 200


class Register(Resource):
    def get(self):
        return 200

    def post(self):
        account_type = request.form['account_type']
        username = request.form['username']
        password = request.form['password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']

        if account_type in ['teacher', 'student']:
            register_func = teacher.create_teacher if account_type == 'teacher' else student.create_student
            result = register_func(first_name, last_name, username, password)
            if result:
                return 201

        return 400
