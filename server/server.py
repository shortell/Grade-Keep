from flask_cors import CORS
from flask_restful import Api
from flask_session import Session
from flask import Flask, session
from db import db_utils
from rest_api.auth_api import *
from rest_api.teacher_api import *
from rest_api.student_api import *



app = Flask(__name__)  # create Flask instance
app.config['SECRET_KEY'] = '3d6f45a5fc12445dbac2f59c3b6c7cb1'  # change on deployment
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = "C:\\Users\\jacks\\Software_Engineer\\Personal\\Grade-Keep\\server\\flask_session"
app.config['SESSION_KEY_PREFIX'] = 'GradeKeep'
app.config.from_object(__name__)
app.config.update(SESSION_COOKIE_SAMESITE="None", SESSION_COOKIE_SECURE=True)
Session(app)
CORS(app)  # Enable CORS on Flask server to work with Nodejs pages
api = Api(app)  # api router

# URLs
teacher_url = "/teacher"
student_url = "/student"
course_url = "/courses/<int:course_id>"
assignment_url = "/assignments/<int:assignment_id>"
grade_url = "/grades/<int:grade_id>"

# Authentication
api.add_resource(Login, "/login")
api.add_resource(Logout, "/logout")
api.add_resource(Register, "/register")

# Teacher resources
api.add_resource(Teachers, teacher_url)
api.add_resource(T_Courses, teacher_url + "/courses")
api.add_resource(T_Course, teacher_url + course_url)
api.add_resource(T_Students, teacher_url + course_url + "/students")
api.add_resource(T_Student, teacher_url + course_url + "/students/<int:enrollment_id>")
api.add_resource(T_Assignments, teacher_url + course_url + "/assignments")
api.add_resource(T_Assignment, teacher_url + course_url + assignment_url)
api.add_resource(T_Submissions, teacher_url + course_url + assignment_url + "/submissions")
api.add_resource(T_Submission, teacher_url + course_url + assignment_url + "/submissions/<int:submission_id>")
api.add_resource(T_Grades, teacher_url + course_url + "/grades")
api.add_resource(T_Grade, teacher_url + course_url + grade_url)
api.add_resource(T_Scores, teacher_url + course_url + grade_url + "/scores")
api.add_resource(T_Score, teacher_url + course_url + grade_url + "/scores/<int:score_id>")

# Student resources
api.add_resource(Students, student_url)
api.add_resource(S_Courses, student_url + "/courses")
api.add_resource(S_Course, student_url + course_url)
api.add_resource(S_Assignments, student_url + course_url + "/assignments")
api.add_resource(S_Assignment, student_url + course_url + assignment_url)
api.add_resource(S_Submissions, student_url + course_url + assignment_url + "/submissions")
api.add_resource(S_Submission, student_url + course_url + assignment_url + "/submissions/<int:submission_id>")
api.add_resource(S_Grades, student_url + course_url + "/grades")
api.add_resource(S_Scores, student_url + course_url + grade_url + "/scores")




if __name__ == '__main__':
    db_utils.initialize_database()
    db_utils.seed_database()
    app.run(debug=True)
    app
    print(session + " server.py")