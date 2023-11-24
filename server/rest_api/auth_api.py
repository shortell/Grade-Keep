from flask import session, make_response
from flask_restful import Resource, request
from db import teacher, student


class Login(Resource):
    def get(self):
        return make_response("OK", 200)

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
                print(session + " auth_api.py")
                return make_response("Successfully logged in", 200)

        return make_response("login failed", 400)


class Logout(Resource):
    def get(self):
        session.clear()
        return make_response("OK", 200)


class Register(Resource):
    def get(self):
        return make_response("OK", 200)

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
                return make_response("Account registered", 201)
            return make_response("username \"{0}\" is taken".format(username), 400)
        return make_response("Account type \"{0}\" not valid".format(account_type), 400)
