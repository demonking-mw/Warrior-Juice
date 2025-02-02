"""
Naming logic: 
classname_action

Commenting:
what for, what is required
"""

from flask_restful import reqparse


# user login: user_name and pwd
user_login = reqparse.RequestParser()
user_login.add_argument(
    "user_name", type=str, help="User name is required", required=True
)
user_login.add_argument("pwd", type=str, help="Password is required", required=True)


# user registration: user_name, email, and pwd
user_regis = reqparse.RequestParser()
user_regis.add_argument(
    "user_name", type=str, help="User name is required", required=True
)
user_regis.add_argument("email", type=str, help="Email is required", required=True)
user_regis.add_argument("pwd", type=str, help="Password is required", required=True)
