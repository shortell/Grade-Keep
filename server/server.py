from flask_cors import CORS
from flask_restful import Api
from flask import Flask
from rest_api.auth_api import Login, Logout, Register
from rest_api.teacher_api import (Teachers, Courses, Course, Assignments,
                                  Assignment, Students, Student, Submissions, Submission, Grades, Grade, Scores, Score)
from db import db_utils


app = Flask(__name__)  # create Flask instance
app.config['SECRET_KEY'] = 'dev'  # change on deployment
CORS(app)  # Enable CORS on Flask server to work with Nodejs pages
api = Api(app)  # api router
course_url = "/teachers/courses/<int:course_id>"
assignment_url = "/assignments/<int:assignment_id>"
grade_url = "/grades/<int:grade_id>"
# TEACHER RESOURCES
api.add_resource(Login, "/login")
api.add_resource(Logout, "/logout")
api.add_resource(Register, "/register")
api.add_resource(Teachers, "/teachers")
api.add_resource(Courses, "/teachers/courses")
api.add_resource(Course, course_url)
api.add_resource(Students, course_url + "/students")
api.add_resource(Student, course_url + "/students/<int:enrollment_id>")
api.add_resource(Assignments, course_url + "/assignments")
api.add_resource(Assignment, course_url + assignment_url)
api.add_resource(Submissions, course_url + assignment_url + "/submissions")
api.add_resource(Submission, course_url + assignment_url + "/submissions/<int:submission_id>")
api.add_resource(Grades, course_url + "/grades")
api.add_resource(Grade, course_url + grade_url)
api.add_resource(Scores, course_url + grade_url + "/scores")
api.add_resource(Score, course_url + grade_url + "/scores/<int:score_id>")


if __name__ == '__main__':
    db_utils.initialize_database()
    db_utils.seed_database()
    app.run(debug=True),  # starts Flask
