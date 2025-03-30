"""
Operations around activities
"""

# pylint: disable=import-error
import json
from flask_restful import Resource
import psycopg

from backend.flask_api import dbconn, input_req_act as input_req
from backend.logic_classes import user_name_flatten as unf
from backend.logic_classes import build_qparser
from backend.logic_classes import userinfo_edit
from backend.logic_classes import activity_actions as aa


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
        activity_act = aa.ActivityActions(database, args)
        result, code = activity_act.get()
        database.close()
        # Ensure result is JSON serializable
        result = json.loads(json.dumps(result, default=str))
        return result, code

    def post(self):
        """
        Create an activity
        Update user account with the new activity
        """
        args = input_req.activity_create.parse_args()
        database = dbconn.DBConn()
        activity_act = aa.ActivityActions(database, args)
        new_act_id, stat = activity_act.create_act()
        if not stat:
            database.close()
            return {"status": False, "detail": "creation failed"}, 400
        psudoargs = {
            "reauth_jwt": args["reauth_jwt"],
            "uid": args["uid"],
            "act_ids": str(new_act_id),
            "sess_ids": "",
        }
        user_info_edit = userinfo_edit.UserInfoEdit(database, psudoargs)
        result, code = user_info_edit.post()
        database.close()
        return result, code

    def put(self):
        """
        update an activity
        """
        args = input_req.activity_mod.parse_args()
        database = dbconn.DBConn()
        activity_act = aa.ActivityActions(database, args)
        if args["is_crit"]:
            result, code = activity_act.update_crit()
            database.close()
            return result, code
        return {"status": False, "detail": "monkey"}, 500
        # Non-crit update not built yet

        # # Create the activity
        # args = input_req.activity_create.parse_args()

        # # Define the columns and corresponding values

        # post_targets = ["act_type", "due_date", "act_brief", "aux_info", "task_tree"]
        # columns, values, params = build_qparser.qparser(post_targets, args)

        # columns.extend(["act_title", "user_name", "admin_user_name"])
        # values.extend(["%s", "%s", "%s"])
        # params.append(args["act_title"])
        # params.append(json.dumps(args["user_name"]))
        # params.append(json.dumps(args["admin_user_name"]))
        # # Generate SQL query
        # sql_query = f"""
        #     INSERT INTO activity ({', '.join(columns)})
        #     VALUES ({', '.join(values)})
        #     RETURNING act_id;
        # """

        # # Execute SQL query
        # try:
        #     act_id = database.run_sql(sql_query, params)
        # except Exception as e:
        #     database.close()
        #     return {
        #         "status": False,
        #         "detail": {
        #             "status": "activity creation failed with error",
        #             "detail": str(e),
        #         },
        #     }, 400

        # # Add it to each user, include the userid in the return if they dne
        # user_list = unf.user_flatten(args["user_name"])
        # failed_users = []

        # for user_name in user_list:
        #     sql_query = f"SELECT user_act_list FROM user_accounts WHERE user_name = '{user_name}';"
        #     try:
        #         act_list = database.run_sql(sql_query)
        #     except psycopg.errors.UndefinedColumn:
        #         failed_users.append(user_name)
        #         continue
        #     if not act_list:
        #         failed_users.append(user_name)
        #         continue
        #     activity_list = act_list[0]["user_act_list"]
        #     activity_list.append(act_id[0]["act_id"])
        #     sql_query = f"UPDATE user_accounts SET user_act_list = ARRAY{activity_list} WHERE user_name = '{user_name}';"
        #     print("DEBUG: activity list")
        #     print(activity_list)
        #     try:
        #         database.run_sql(sql_query)
        #     except Exception as e:
        #         print("FAILURE REASON:")
        #         print(str(e))
        #         failed_users.append(user_name)
        # database.close()
        # return {
        #     "status": True,
        #     "detail": {
        #         "status": "activity created with existing users updated",
        #         "failed": failed_users,
        #     },
        # }, 201
