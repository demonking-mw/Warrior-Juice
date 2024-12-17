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

class UserAccountModel(db.Model):
    '''
    User Account Model
    '''
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String(150), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f"UserAccountModel('{self.username}', '{self.email}', '{self.date_created}')"

user_args = reqparse.RequestParser()

@app.route('/')
def home() -> str:
    '''
    test 
    '''
    return '<h1>Warrior Juice API test, hello world!</h1>'

if __name__ == '__main__':
    app.run(debug=True)
