"""
Operations around activities
"""

from flask import Flask
from flask_restful import Api, Resource, reqparse
import psycopg
from backend.flask_api import dbconn, input_req


class Activity(Resource):
    """
    Handles activity operations
    """

    def get(self):
        """
        Get activities, specification by the input json
        Options: by user (all), by id, by user and id (for validation)
        """
        args = input_req.activity_get.parse_args()
        database = dbconn.DBConn()
        if args["get_all"]:
            # Gets all activities for a user
            if args["user_name"] is None:
                # Bad input
                database.close()
                return {
                    "status": False,
                    "detail": {
                        "status": "get_all requires user, but no user was given"
                    },
                }, 400
            sql_query = f"SELECT user_act_list FROM user_accounts WHERE user_name = '{args['user_name']}';"
            try:
                act_list = database.run_sql(sql_query)
            except psycopg.errors.UndefinedColumn as e:
                database.close()
                return {
                    "status": False,
                    "detail": {"status": "user not found", "detail": e},
                }, 400
            if not act_list:
                database.close()
                return {"status": False, "detail": {"status": "user not found"}}, 400
            user_acts = act_list[0]["user_act_list"]
            # user_acts must only contain one item since user_name is primary key
            all_activities = []  # list of jsons
            dne_activities = []  # list of ids
            for activity_id in user_acts:
                sql_query = f"SELECT * FROM activity WHERE act_id = '{activity_id}';"
                try:
                    act = database.run_sql(sql_query)
                    if act:
                        all_activities.append(act[0])
                    else:
                        dne_activities.append(activity_id)
                except psycopg.errors.UndefinedColumn as e:
                    dne_activities.append(activity_id)
            database.close()
            if len(all_activities) != 0:
                return {
                    "status": True,
                    "detail": {"activities": all_activities, "failed": dne_activities},
                }, 200
            else:
                return {
                    "status": False,
                    "detail": {
                        "status": "no activities found",
                        "failed": dne_activities,
                    },
                }, 400
        else:
            # Get a specific activity, either by id or by user and id
            if args["act_id"] is None:
                return {
                    "status": False,
                    "detail": {
                        "status": "get_all requires act_id, but no act_id was given"
                    },
                }, 400
            sql_query = f"SELECT * FROM activity WHERE act_id = '{args['act_id']}';"
            try:
                act = database.run_sql(sql_query)
                database.close()
                if act and args["user_name"] is None:
                    return {
                        "status": True,
                        "detail": {
                            "status": "obtained activity without user info",
                            "activity": act[0],
                        },
                    }, 200
                elif act and args["user_name"] in act[0]["user_name"].values():
                    return {
                        "status": True,
                        "detail": {
                            "status": "obtained activity, user have access to it",
                            "activity": act[0],
                        },
                    }, 200
                else:
                    return {
                        "status": False,
                        "detail": {
                            "status": "activity not found or user does not have access"
                        },
                    }, 400
            except psycopg.errors.UndefinedColumn as e:
                database.close()
                return {
                    "status": False,
                    "detail": {"status": "activity not found", "detail": e},
                }, 400
