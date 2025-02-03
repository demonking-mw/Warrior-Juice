"""
Operations around activities
"""

import json
from flask import Flask
from flask_restful import Api, Resource, reqparse
import psycopg

from backend.flask_api import dbconn, input_req
from backend.logic_classes import user_name_flatten as unf


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
                elif act and args["user_name"] in unf.user_flatten(act[0]["user_name"]):
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

    def post(self):
        """
        Create an activity
        Updates all user accounts with the new activity
        """
        args = input_req.activity_create.parse_args()
        database = dbconn.DBConn()
        # Create the activity
        args = input_req.activity_create.parse_args()

        # Define the columns and corresponding values
        columns = ["act_title", "user_name"]
        values = ["%s", "%s"]
        params = [args["act_title"], json.dumps(args["user_name"])]

        if args.get("act_type"):
            columns.append("act_type")
            values.append("%s")
            params.append(args["act_type"])

        if args.get("due_date"):
            columns.append("due_date")
            values.append("%s")
            params.append(args["due_date"])

        if args.get("act_brief"):
            columns.append("act_brief")
            values.append("%s")
            params.append(args["act_brief"])

        if args.get("aux_info"):
            columns.append("act_aux_info")
            values.append("%s")
            params.append(json.dumps(args["aux_info"]))

        if args.get("task_tree"):
            columns.append("tasks_tree")
            values.append("%s")
            params.append(json.dumps(args["task_tree"]))

        # Generate SQL query
        sql_query = f"""
            INSERT INTO activity ({', '.join(columns)})
            VALUES ({', '.join(values)})
            RETURNING act_id;
        """

        # Execute SQL query
        try:
            act_id = database.run_sql(sql_query, params)
        except Exception as e:
            database.close()
            return {
                "status": False,
                "detail": {
                    "status": "activity creation failed with error",
                    "detail": str(e),
                },
            }, 400

        # Add it to each user, include the userid in the return if they dne
        user_list = unf.user_flatten(args["user_name"])
        failed_users = []

        for user_name in user_list:
            sql_query = f"SELECT user_act_list FROM user_accounts WHERE user_name = '{user_name}';"
            try:
                act_list = database.run_sql(sql_query)
            except psycopg.errors.UndefinedColumn as e:
                failed_users.append(user_name)
                continue
            if not act_list:
                failed_users.append(user_name)
                continue
            activity_list = act_list[0]["user_act_list"]
            activity_list.append(act_id[0]["act_id"])
            sql_query = f"UPDATE user_accounts SET user_act_list = ARRAY{activity_list} WHERE user_name = '{user_name}';"
            print("DEBUG: activity list")
            print(activity_list)
            try:
                database.run_sql(sql_query)
            except Exception as e:
                print("FAILURE REASON:")
                print(str(e))
                failed_users.append(user_name)
        database.close()
        return {
            "status": True,
            "detail": {
                "status": "activity created with existing users updated",
                "failed": failed_users,
            },
        }, 201
