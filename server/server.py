from flask import Flask
from flask_restful import Api
from flask_cors import CORS


app = Flask(__name__) #create Flask instance
CORS(app) #Enable CORS on Flask server to work with Nodejs pages
api = Api(app) #api router

@app.route('/')
def home():
    return "Hello"



if __name__ == '__main__':
    app.run(debug=True), #starts Flask