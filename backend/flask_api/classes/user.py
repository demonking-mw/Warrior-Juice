"""
Operations around users
"""

from flask import Flask
from flask_restful import Api, Resource, reqparse
import psycopg
from backend.flask_api import dbconn, input_req


class User(Resource):
    """
    dbconn pooling not used, very slow for now
    deals with users
    """

    def get(self):
        """
        gets the user details with username and password
        """
        args = input_req.user_login.parse_args()
        database = dbconn.DBConn()
        sql_query = (
            f"SELECT * FROM user_accounts WHERE user_name = '{args['user_name']}';"
        )
        try:
            table_1 = database.run_sql(sql_query)
            database.close()
        except psycopg.errors.UndefinedColumn as e:
            database.close()
            return {
                "status": False,
                "detail": {"status": "user not found", "detail": str(e)},
            }, 400
        if not table_1:
            return {"status": False, "detail": {"status": "user not found"}}, 400
        if table_1 and table_1[0]["pwd"] == args["pwd"]:
            return {"status": True, "detail": table_1[0]}, 200
        else:
            return {"status": False, "detail": {"status": "password incorrect"}}

    def post(self):
        """
        creates a new user with username, email, and password
        no email varification, add here in the future
        """
        args = input_req.user_regis.parse_args()
        database = dbconn.DBConn()
        sql_query = f"INSERT INTO user_accounts VALUES('{args['user_name']}', '{args['pwd']}', '{args['email']}', 'tier1', ARRAY[]::integer[], ARRAY[]::integer[], '{{}}'::jsonb)"
        try:
            database.run_sql(sql_query)
            database.close()
            return {"status": True, "detail": {"status": "user created"}}, 201
        except psycopg.errors.UniqueViolation as e:
            database.close()
            return {
                "status": False,
                "detail": {"status": "user already exists", "detail": str(e)},
            }, 200

    def put(self):
        """
        returns status as boolean of whether action is successful
        To avoid confusion, only one action can be performed at a time
        Operation logic: old password is mandatory for changing email, optional for changing password
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
                        "status": f"password changed for user '{args['user_name']}' after successful external auth"
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
                    "detail": {"status": f"user '{args['user_name']}' deleted", "detail": user_info},
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
                    sql_query = f"SELECT * FROM activity WHERE act_id = '{activity_id}';"
                    try:
                        act = database.run_sql(sql_query)
                        if not act:
                            activities_list.remove(activity_id)
                    except psycopg.errors.UndefinedColumn as e:
                        activities_list.remove(activity_id)
                sql_query = f"UPDATE user_accounts SET activities = '{activities_list}' WHERE user_name = '{args['user_name']}';"
                try:
                    database.run_sql(sql_query)
                    database.close()
                except Exception as e:
                    database.close()
                    return {
                        "status": False,
                        "detail": {"status": "error purging activities", "detail": str(e)},
                    }, 400
                return {
                    "status": True,
                    "detail": {"status": "purged activities", "detail": activities_list},
                }, 200
            else:
                return {
                    "status": False,
                    "detail": {"status": "password incorrect, not deleted"},
                }, 400
        else:
            database.close()
            return {"status": False, "detail": {"status": "unknown action"}}, 400
