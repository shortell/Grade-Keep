from flask_cors import CORS
from flask_restful import Api
from flask import Flask
from routes.auth_api import Login, Register
from routes.teacher_api import Teacher
from db import db_utils


app = Flask(__name__)  # create Flask instance
app.config['SECRET_KEY'] = 'dev'  # change on deployment
CORS(app)  # Enable CORS on Flask server to work with Nodejs pages
api = Api(app)  # api router
api.add_resource(Login, "/login")
api.add_resource(Register, "/register")
api.add_resource(Teacher, "/teachers/")


if __name__ == '__main__':
    db_utils.initialize_database()
    db_utils.seed_database()
    app.run(debug=True),  # starts Flask
