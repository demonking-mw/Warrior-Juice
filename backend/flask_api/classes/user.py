"""
Operations around users
"""

# pylint: disable=import-error
from flask import Flask, make_response
from flask_restful import Api, Resource, reqparse
import psycopg
from backend.flask_api import dbconn, input_req
from backend.logic_classes import user_name_flatten as unf
from backend.logic_classes import google_auth_extract as ga_ext
from backend.logic_classes import user_auth


class User(Resource):
    """
    dbconn pooling not used, very slow for now
    deals with users
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
            user_auth_obj = user_auth.UserAuth(auth_jwt.decoded)
            user_auth_json, login_status = user_auth_obj.auth_go()
            if login_status == -1:
                print("ERROR: something is cooked for login")
                return {"status": False, "detail": {"status": "info mismatch"}}, 400
            else:
                return user_auth_json, login_status
        elif args["type"] == "eup":
            # email user password auth
            if "action" not in args:
                return {"status": False, "detail": {"status": "action missing"}}, 400
            if args["action"] == "login":
                user_auth_obj = user_auth.UserAuth(args)
                user_auth_json, login_status = user_auth_obj.login_up()
                if login_status == -1:
                    print("ERROR: something is cooked for login")
                    return {"status": False, "detail": {"status": "info mismatch"}}, 400
                else:
                    return user_auth_json, login_status
            elif args["action"] == "signup":
                pass
            else:
                return {"status": False, "detail": {"status": "unknown action"}}, 400
        else:
            return {"status": False, "detail": {"status": "unknown type"}}, 400

    def put(self):
        """
        returns status as boolean of whether action is successful
        To avoid confusion, only one action can be performed at a time
        Operation logic:
        old password is mandatory for changing email, optional for changing password
        Auth can be used to change password
        Purge: delete every activity that DNE
        Action: change, mod_tier, delete, (upcoming) purge
        """
        args = input_req.user_modify.parse_args()
        database = dbconn.DBConn()
        # change user details, password or email
        try:
            # gets user info and return error if not found
            sql_query = (
                f"SELECT * FROM user_accounts WHERE user_name = '{args['user_name']}';"
            )
            user_info = database.run_sql(sql_query)
        except psycopg.errors.UndefinedColumn as e:
            database.close()
            return {
                "status": False,
                "detail": {"status": "user not found", "detail": str(e)},
            }, 400
        if not user_info:
            database.close()
            return {"status": False, "detail": {"status": "user not found"}}, 400
        # this ensures the user in question exists
        if args["action"] == "change":
            if args["pwd"] is not None:
                # if pwd is provided, then assume user want to change password knowing old password
                if user_info and user_info[0]["pwd"] == args["pwd"]:
                    # if the old password is correct
                    if args["new_pwd"] is not None:
                        # change password to new password
                        sql_query = f"UPDATE user_accounts SET pwd = '{args['new_pwd']}' WHERE user_name = '{args['user_name']}';"
                        database.run_sql(sql_query)
                        database.close()
                        return {
                            "status": True,
                            "detail": {
                                "status": f"password changed for user '{args['user_name']}'"
                            },
                        }, 200
                    elif args["email"] is not None:
                        # change email to new email
                        sql_query = f"UPDATE user_accounts SET email = '{args['email']}' WHERE user_name = '{args['user_name']}';"
                        database.run_sql(sql_query)
                        database.close()
                        return {
                            "status": True,
                            "detail": {
                                "status": f"email changed for user '{args['user_name']}'"
                            },
                        }, 200
                    else:
                        # no action done but old password is correct
                        database.close()
                        return {
                            "status": True,
                            "detail": {"status": "no action done"},
                        }, 200
                else:
                    database.close()
                    return {
                        "status": False,
                        "detail": {"status": "old password incorrect"},
                    }, 400
            elif True:
                # For future: insert auth/email verification stuff in place of True
                # Alternatively, use info in args["detail"] to authenticate
                sql_query = f"UPDATE user_accounts SET pwd = '{args['new_pwd']}' WHERE user_name = '{args['user_name']}';"
                database.run_sql(sql_query)
                database.close()
                return {
                    "status": True,
                    "detail": {
                        "status": f"password changed for user '{args['user_name']}'"
                    },
                }, 200
            else:
                database.close()
                return {
                    "status": False,
                    "detail": {"status": "old password not provided and auth failed"},
                }, 400
        elif args["action"] == "mod_tier":
            if True:
                # For future: insert auth/email verification stuff in place of True
                # Alternatively, use info in args["detail"] to authenticate
                sql_query = f"UPDATE user_accounts SET acc_type = '{args['tier']}' WHERE user_name = '{args['user_name']}';"
                database.run_sql(sql_query)
                database.close()
                return {
                    "status": True,
                    "detail": {
                        "status": f"tier changed for user '{args['user_name']}'"
                    },
                }, 200
            else:
                database.close()
                return {"status": False, "detail": {"status": "auth failed"}}, 400
        elif args["action"] == "delete":
            # password is mandatory for deleting account, add auth later
            if user_info and user_info[0]["pwd"] == args["pwd"]:
                sql_query = f"DELETE FROM user_accounts WHERE user_name = '{args['user_name']}';"
                try:
                    database.run_sql(sql_query)
                    database.close()
                except Exception as e:
                    database.close()
                    return {
                        "status": False,
                        "detail": {"status": "error deleting user", "detail": str(e)},
                    }, 400
                return {
                    "status": True,
                    "detail": {
                        "status": f"user '{args['user_name']}' deleted",
                        "detail": user_info,
                    },
                }, 200
            else:
                database.close()
                return {
                    "status": False,
                    "detail": {"status": "password incorrect, not deleted"},
                }, 400
        elif args["action"] == "purge":
            # delete all activities that DNE
            if user_info and user_info[0]["pwd"] == args["pwd"]:
                activities_list = user_info[0]["activities"]
                for activity_id in activities_list:
                    sql_query = (
                        f"SELECT * FROM activity WHERE act_id = '{activity_id}';"
                    )
                    try:
                        act = database.run_sql(sql_query)
                        if not act:
                            activities_list.remove(activity_id)
                        act_user_list = unf.user_flatten(act[0]["user_name"])
                        if args["user_name"] not in act_user_list:
                            # user does not have access to this activity
                            activities_list.remove(activity_id)
                    except psycopg.errors.UndefinedColumn:
                        activities_list.remove(activity_id)
                sql_query = f"UPDATE user_accounts SET activities = '{activities_list}' WHERE user_name = '{args['user_name']}';"
                try:
                    database.run_sql(sql_query)
                    database.close()
                except Exception as e:
                    database.close()
                    return {
                        "status": False,
                        "detail": {
                            "status": "error purging activities",
                            "detail": str(e),
                        },
                    }, 400
                return {
                    "status": True,
                    "detail": {
                        "status": "purged activities",
                        "detail": activities_list,
                    },
                }, 200
            else:
                return {
                    "status": False,
                    "detail": {"status": "password incorrect, not deleted"},
                }, 400
        else:
            database.close()
            return {"status": False, "detail": {"status": "unknown action"}}, 400
