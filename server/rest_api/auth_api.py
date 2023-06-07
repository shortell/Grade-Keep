from flask import session
from flask_restful import Resource, request
from db import teacher, student


class Login(Resource):
    def get(self):
        return 200

    def post(self):
        data = request.get_json()
        account_type = data.get('account_type')
        username = data.get('username')
        password = data.get('password')

        if account_type in ['teacher', 'student']:
            login_func = teacher.login if account_type == 'teacher' else student.login
            result = login_func(username, password)

            if result is not None:
                session['account_type'] = account_type
                session['id'] = result[0]
                print("logged in")
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
        data = request.get_json()
        account_type = data.get('account_type')
        username = data.get('username')
        password = data.get('password')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        if account_type in ['teacher', 'student']:
            register_func = teacher.create_teacher if account_type == 'teacher' else student.create_student
            result = register_func(first_name, last_name, username, password)
            if result:
                print("account created")
                return 201
            return {403: "username taken"}
        
