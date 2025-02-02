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


# modify user: username, pwd(not mandatory), new_pwd, email, tier, detail
user_modify = reqparse.RequestParser()
user_modify.add_argument(
    "action",
    type=str,
    help="Action is required, can be change or mod_tier or ...",
    required=True,
)
user_modify.add_argument(
    "user_name", type=str, help="User name is required", required=True
)
user_modify.add_argument("pwd", type=str, help="Old password, for auth", required=False)
user_modify.add_argument("new_pwd", type=str, help="New password", required=False)
user_modify.add_argument("email", type=str, help="New email", required=False)
user_modify.add_argument("tier", type=str, help="Updated tier", required=False)
user_modify.add_argument(
    "detail", type=str, help="Auth info to mode tier or new pwd", required=False
)
