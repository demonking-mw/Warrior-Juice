"""
Operations around activities
"""

# pylint: disable=import-error
import json
from flask import Flask
from flask_restful import Api, Resource, reqparse
import psycopg

from backend.flask_api import dbconn, input_req
from backend.logic_classes import user_name_flatten as unf
from backend.logic_classes import build_qparser


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
                except psycopg.errors.UndefinedColumn:
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

        post_targets = ["act_type", "due_date", "act_brief", "aux_info", "task_tree"]
        columns, values, params = build_qparser.qparser(post_targets, args)

        columns.extend(["act_title", "user_name", "admin_user_name"])
        values.extend(["%s", "%s", "%s"])
        params.append(args["act_title"])
        params.append(json.dumps(args["user_name"]))
        params.append(json.dumps(args["admin_user_name"]))
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
            except psycopg.errors.UndefinedColumn:
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

    def put(self):
        """
        Update a task, for subtask tree, a new tree is required
        """
        args = input_req.activity_modify.parse_args()
        database = dbconn.DBConn()
        # Get the activity and confirm the user has access to actions

        sql_query = f"SELECT * FROM activity WHERE act_id = '{args['act_id']}';"
        try:
            act = database.run_sql(sql_query)
            if not act:
                database.close()
                return {
                    "status": False,
                    "detail": {"status": "activity not found"},
                }, 400
        except psycopg.errors.UndefinedColumn as e:
            database.close()
            return {
                "status": False,
                "detail": {"status": "activity not found", "detail": e},
            }, 400
        if args["user_name"] not in unf.user_flatten(act[0]["user_name"]):
            database.close()
            return {
                "status": False,
                "detail": {"status": "user does not have access to activity"},
            }, 400
        # At this point, the user has access to the activity
        # Check if user_name is in admin_user_name array
        admin_access = True
        if args["user_name"] not in act[0]["admin_user_name"]:
            admin_access = False
        # Update the activity
        if args["action"] == "update":
            # Update the activity
            put_targets = [
                "act_title",
                "act_type",
                "due_date",
                "act_brief",
                "aux_info",
                "task_tree",
            ]
            columns, values, params = build_qparser.qparser(put_targets, args)
            # Permission required for below fields
            if args.get("user_name_tree") and admin_access:
                columns.append("user_name_tree")
                values.append("%s")
                params.append(json.dumps(args["user_name_tree"]))
            if args.get("admin_user_name") and admin_access:
                columns.append("admin_user_name")
                values.append("%s")
                params.append(json.dumps(args["admin_user_name"]))
            if len(columns) == 0:
                database.close()
                return {
                    "status": False,
                    "detail": {
                        "status": "no fields to update",
                        "admin_access": admin_access,
                    },
                }, 400
            sql_query = f"""
                UPDATE activity
                SET {', '.join([f'{col} = %s' for col in columns])}
                WHERE act_id = '{args['act_id']}';
            """
            try:
                database.run_sql(sql_query, params)
            except Exception as e:
                database.close()
                return {
                    "status": False,
                    "detail": {"status": "activity update failed", "detail": str(e)},
                }, 400
            database.close()
            return {
                "status": True,
                "detail": {"status": "activity updated", "admin_access": admin_access},
            }, 200
        elif args["action"] == "delete":
            # Delete the activity
            if admin_access:
                sql_query = f"DELETE FROM activity WHERE act_id = '{args['act_id']}';"
                try:
                    database.run_sql(sql_query)
                    database.close()
                except Exception as e:
                    database.close()
                    return {
                        "status": False,
                        "detail": {
                            "status": "activity deletion failed",
                            "detail": str(e),
                        },
                    }, 400
                return {
                    "status": True,
                    "detail": {
                        "status": "activity deleted",
                        "user_name_tree": act[0]["user_name"],
                        "admin_list": act[0]["admin_user_name"],
                    },
                }, 200
                # Purge should be calle separately
        else:
            # Invalid action
            database.close()
            return {
                "status": False,
                "detail": {"status": "invalid action"},
            }, 400
