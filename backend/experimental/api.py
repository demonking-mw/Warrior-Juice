"""
Experimental backend with local db
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, reqparse, fields, marshal_with, abort


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
api = Api(app)



user_args = reqparse.RequestParser()

@app.route('/')
def home() -> str:
    '''
    test 
    '''
    return '<h1>Warrior Juice API test, hello world!</h1>'

if __name__ == '__main__':
    app.run(debug=True)
