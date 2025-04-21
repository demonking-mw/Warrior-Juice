"""
Operations around users
"""

# pylint: disable=import-error
from flask_restful import Resource
from backend.flask_api import input_req_user as input_req
from backend.logic_classes.helpers import google_auth_extract as ga_ext
from backend.logic_classes import user_auth, admin_user_edit as aue
from backend.flask_api import dbconn


class User(Resource):
    """
    Handles the database side of user operations
    Basically the implementation of user_auth.py
    Get is paired with post for auto creation of account with google auth
    """

    def post(self):
        """
        Login AND signup user
        Args:
        type: str: ONEOF(go, jwt, eup, jwt_check)
        - mandatory
        - jwt_check is for login with reauth_jwt
        jwt_token: str: token for go type
        - optional, mandatory for go
        reauth_jwt: str: token for jwt type
        - optional, mandatory for reauth
        - note: this is backend-generated, but jwt_token is from google
        action: str: action for eup type
        - optional, mandatory for eup
        - can be: login or signup or delete
        email: str: email for eup type
        password: str: password for eup type
        Name: str: name for eup type
        """
        args = input_req.user_auth.parse_args()
        if args["type"] == "go":
            # google auth
            if args.get("jwt_token") is None:
                return {"status": False, "detail": {"status": "jwt_token missing"}}, 400
            auth_jwt = ga_ext.GoogleAuthExtract(args["jwt_token"])
            if not auth_jwt.authenticate():
                return {
                    "status": False,
                    "detail": {"status": "auth failed, jwt not good"},
                }, 401
            # Got the jwt token and authed.
            database = dbconn.DBConn()
            user_auth_obj = user_auth.UserAuth(database, auth_jwt.decoded)
            user_auth_json, login_status = user_auth_obj.auth_go()
            database.close()
            if login_status == -1:
                print("ERROR: something is cooked for login")
                return {"status": False, "detail": {"status": "info mismatch"}}, 400
            else:
                return user_auth_json, login_status
        elif args["type"] == "eup":
            # email user password auth
            if "action" not in args:
                return {"status": False, "detail": {"status": "action missing"}}, 400
            database = dbconn.DBConn()
            user_auth_obj = user_auth.UserAuth(database, args)
            if args["action"] == "login":
                user_auth_json, login_status = user_auth_obj.login_up()
            elif args["action"] == "signup":
                user_auth_json, login_status = user_auth_obj.signup_eupn()
            elif args["action"] == "delete":
                user_auth_json, login_status = user_auth_obj.delete_eupn()
            else:
                database.close()
                return {"status": False, "detail": {"status": "unknown action"}}, 400
            database.close()
            if login_status == -1:  # Login_status will be defined if this is reached
                print("ERROR: something is cooked for login")
                return {"status": False, "detail": {"status": "info mismatch"}}, 400
            else:
                return user_auth_json, login_status
        elif args["type"] == "jwt" or args["type"] == "jwt_check":
            # login with a jwt token
            if "reauth_jwt" not in args:
                return {
                    "status": False,
                    "detail": {"status": "reauth_jwt missing"},
                }, 400
            database = dbconn.DBConn()
            user_auth_obj = user_auth.UserAuth(database, args)
            if args["type"] == "jwt":
                user_auth_json, login_status = user_auth_obj.login_jwt()
            else:
                user_auth_json, login_status = user_auth_obj.login_jwt(True)
            database.close()
            if login_status == -1:
                print("ERROR: something is cooked for login")
                return {"status": False, "detail": {"status": "info mismatch"}}, 400
            else:
                return user_auth_json, login_status
        else:
            return {"status": False, "detail": {"status": "unknown type"}}, 400

    def put(self):
        """
        Edit ADMIN INFO OF USER!!
        Admin: change password, email for eup, change tier, delete user
        this class only handles admin, info is another class
        For email recovery, store a token in the aux_info json in user_account
        Then check it against the input

        Args:
        auth_type: str: auth type, can be eup or go or recover
        - mandatory
        - recover is not fully built yet since smtp is not setup
        uid: str: user id
        - mandatory
        - not changable
        action: str: action to take, can be change or delete
        - mandatory
        - change: change password, email, tier
        - delete: delete user
        jwt_token: str: token for go type
        user_name: str: existing user name
        - optional
        pwd: str: old password, for auth
        - optional, for eup auth
        new_pwd: str: new password
        - for changing
        new_user_name: str: new user name
        - for changing
        auth_str: str: auth string for password recovery
        - NOT BUILT YET
        """
        args = input_req.user_modify.parse_args()
        database = dbconn.DBConn()
        user_info_edit = aue.AdminUserEdit(database, args)
        edit_json = user_info_edit.edit()
        if not edit_json["status"]:
            database.close()
            print(edit_json["detail"])
            return edit_json, 400
        result = user_info_edit.edit()
        database.close()
        if result["status"]:
            return result, 200
        print(edit_json["detail"])
        return result, 400
