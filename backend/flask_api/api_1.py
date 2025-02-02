"""
Experimental backend with local db
run from backend:
python -m api_test.api_1
"""

from flask import Flask
from flask_restful import Api, Resource, reqparse
import psycopg
from . import dbconn
from . import input_req
from .classes.user import User

app = Flask(__name__)
api = Api(app)

api.add_resource(User, "/user")

if __name__ == "__main__":
    app.run(debug=True)
