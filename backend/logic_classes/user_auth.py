"""
Handler for user authentication situations with every login process
Login options: uid/password (up), email/password (ep), google oauth (go)
Signup options: username/password/email (upe), email/password (ep), google oauth (go)
Note: email smtp not supported, yet

On database: eup for email/username/password, go for google oauth

Note: for each method, doccumentation of all possible result is mandatory
"""

from flask_restful import Api, Resource, reqparse  # type: ignore
import psycopg  # type: ignore
from backend.flask_api import dbconn


class UserAuth:
    """
    Class for handling user authentication/creation.
    IS NOT an api endpoint, only parse info
    handles database
    should return a json for user info upon successful login/signup
    The status code is -1 when info is not provided properly
    SHOULD NOT HAPPEN if there is no bug.

    Naming convention: X_Y
    X: action such as login, signup, etc
    Y: method (or req abbrievation)
        go for google oauth
        e for email
        u for uid
        p for pwd
        n for user_name
    """

    def __init__(self, args: dict = None) -> None:
        """
        takes in perspective info in the form of a json with varying fields depending on actions.
        Not having a field for an action will result in failure.
        """
        self.args = args

    def update_args(self, args: dict) -> None:
        """
        updates the args for the class
        """
        self.args = args

    def login_up(self) -> tuple[dict, int]:
        """
        logs in the user with a username and password
        success code start with

        The remaining tuple is the api_ready response

        Expected result: success; user not found; wrongly authed; wrong password
        """
        if "uid" not in self.args or "pwd" not in self.args:
            print("ERROR: uid or pwd not provided")
            return {}, -1
        database = dbconn.DBConn()
        sql_query = f"SELECT * FROM user_accounts WHERE uid = '{self.args['uid']}';"
        table_1 = database.run_sql(sql_query)
        database.close()
        if not table_1:
            return {"status": False, "detail": {"status": "user not found"}}, 400
        if table_1[0]["auth_type"] != "eup":
            return {"status": False, "detail": {"status": "auth type mismatch"}}, 401
        if table_1[0]["pwd"] == self.args["pwd"]:
            return {"status": True, "detail": table_1[0]}, 200
        else:
            return {"status": False, "detail": {"status": "password incorrect"}}, 401

    def signup_eupn(self) -> tuple[dict, int]:
        """
        signs up the user with email, uid, password (and name)

        Expected result: success; uid unique violation
        """
        required_fields = ["uid", "pwd", "email", "user_name"]
        if any(field not in self.args for field in required_fields):
            print("ERROR: uid, pwd, email, or name not provided")
            return {}, -1
        database = dbconn.DBConn()
        sql_query = f"INSERT INTO user_accounts VALUES('{self.args['uid']}', '{self.args['user_name']}', '{self.args['pwd']}', '{self.args['email']}', false, 'eup', 'tier1', ARRAY[]::integer[], ARRAY[]::integer[], '{{}}'::jsonb, 0, '{{}}'::jsonb)"
        try:
            database.run_sql(sql_query)
            database.close()
            return {"status": True, "detail": {"status": "user created"}}, 201
        except psycopg.errors.UniqueViolation:
            database.close()
            print("UID unique violation")
            return {"status": False, "detail": {"status": "uid unique violation"}}, 409

    def delete_eupn(self) -> tuple[dict, int]:
        """
        delete user with email, uid, password (and name)
        TO BE MIGRATED TO admin_user_edit.py
        Expected result: success; deletion failed (return specific error)
        """
        required_fields = ["uid", "pwd", "email", "user_name"]
        if any(field not in self.args for field in required_fields):
            print("ERROR: uid, pwd, email, or name not provided")
            return {}, -1
        database = dbconn.DBConn()
        sql_query = f"DELETE FROM user_accounts WHERE uid = '{self.args['uid']}' AND pwd = '{self.args['pwd']}' AND email = '{self.args['email']}' AND user_name = '{self.args['user_name']}';"
        try:
            database.run_sql(sql_query)
            database.close()
            return {"status": True, "detail": {"status": "user deleted"}}, 200
        except Exception as e:  # pylint: disable=broad-except
            database.close()
            print(f"ERROR: {e}")
            return {
                "status": False,
                "detail": {"status": "deletion failed", "detail": str(e)},
            }, 500

    def auth_go(self) -> tuple[dict, int]:
        """
        logs in the user with google oauth
        success code start with
        The remaining tuple is the api_ready response

        Expected result: success login; success signup; wrongly authed (upon login)
        """
        if "sub" not in self.args:
            print("ERROR: sub not provided")
            return {}, -1
        database = dbconn.DBConn()
        sql_query = f"SELECT * FROM user_accounts WHERE uid = '{self.args['sub']}';"
        table_1 = database.run_sql(sql_query)

        if not table_1:
            sql_query = f"INSERT INTO user_accounts VALUES('{self.args['sub']}', '{self.args['name']}', '', '{self.args['email']}', true, 'go', 'tier1', ARRAY[]::integer[], ARRAY[]::integer[], '{{}}'::jsonb, 0, '{{}}'::jsonb)"
            try:
                database.run_sql(sql_query)
                database.close()
                return {"status": True, "detail": {"status": "user created"}}, 201
            except psycopg.errors.UniqueViolation:
                database.close()
                print("BACKEND ERROR: on creation while account exists")
                return {}, -1
        if table_1[0]["auth_type"] != "go":
            database.close()
            return {"status": False, "detail": "auth type mismatch"}, 401
        database.close()
        return {"status": True, "detail": table_1[0]}, 200
