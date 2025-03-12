"""
Operations around users
"""

# pylint: disable=import-error
from flask_restful import Resource
from backend.flask_api import input_req
from backend.logic_classes import google_auth_extract as ga_ext
from backend.logic_classes import user_auth, admin_user_edit as aue
from backend.flask_api import dbconn


class UserInfo(Resource):
    """
    Handles the modification of user info
    Such as: user_act_list, user_sess_id, etc
    """


class User(Resource):
    """
    Handles the database side of user operations
    Basically the implementation of user_auth.py
    """

    def post(self):
        """
        Handles auth.
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
        elif args["type"] == "jwt":
            # login with a jwt token
            if "reauth_jwt" not in args:
                return {
                    "status": False,
                    "detail": {"status": "reauth_jwt missing"},
                }, 400
            database = dbconn.DBConn()
            user_auth_obj = user_auth.UserAuth(database, args)
            user_auth_json, login_status = user_auth_obj.login_jwt()
            database.close()
            if login_status == -1:
                print("ERROR: something is cooked for login")
                return {"status": False, "detail": {"status": "info mismatch"}}, 400
            else:
                return user_auth_json, login_status
        elif args["type"] == "jwt_check":
            # login with a jwt token
            if "reauth_jwt" not in args:
                return {
                    "status": False,
                    "detail": {"status": "reauth_jwt missing"},
                }, 400
            database = dbconn.DBConn()
            user_auth_obj = user_auth.UserAuth(database, args)
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
        Edit users
        Two types: admin and info
        Admin: change password, email for eup, change tier, delete user
        this class only handles admin, info is another class
        For email recovery, store a token in the aux_info json in user_account
        Then check it against the input
        """
        args = input_req.user_modify.parse_args()
        database = dbconn.DBConn()
        user_info_edit = aue.AdminUserEdit(database, args)
        edit_json = user_info_edit.authenticate()
        if not edit_json["status"]:
            database.close()
            return edit_json, 400
        result = user_info_edit.edit()
        database.close()
        if result["status"]:
            return result, 200
        return result, 400
