"""
Handles the DB side of activities
Takes in a db object
"""
import json
from datetime import datetime

from backend.logic_classes import user_auth
from backend.logic_classes import user_name_flatten as unf
from backend.flask_api import dbconn


class ActivityActions:
    """
    Default action: auth
    """

    def __init__(self, database: dbconn.DBConn, args: dict = None) -> None:
        """
        takes in perspective info in the form of a json with varying fields depending on actions.
        Not having a field for an action will result in failure.
        """
        self.database = database
        self.args = args
        self.authed = False
        self.new_jwt = None
        auth_class = user_auth.UserAuth(self.database, self.args)
        self.auth_result, self.auth_code = auth_class.login_jwt()
        if self.auth_code == -1:
            print("ERROR:" + str(self.auth_result))

    def get(self) -> tuple[dict, int]:
        """
        Get the activities for the user
        Takes in: uid, reauth_jwt, get_all(bool). act_id(optional)
        """
        if not self.auth_result["status"]:
            return self.auth_result, self.auth_code
        if self.args["get_all"]:
            # NO FAIL CASE HERE
            # Get all activities of the user
            all_act_ids = self.auth_result["detail"]["user_act_list"]
            num_of_acts = len(all_act_ids)
            if not all_act_ids:
                return {"status": True, "detail": {}}, 200
            # using auth, get all acts that belong to the user
            query = "SELECT * FROM activity WHERE act_id = ANY(%s)"
            table_1 = self.database.run_sql(query, (all_act_ids,))
            return {
                "status": True,
                "detail": {"total_count": num_of_acts, "acts": table_1},
            }, 200
        else:
            # Get a single activity, by its id
            # Auth whether the user can see this activity
            if self.args["act_id"] is None:
                return {"status": False, "error": "Missing activity ID"}, 400

            act_id = self.args["act_id"]
            query = "SELECT * FROM activity WHERE act_id = %s"
            table_1 = self.database.run_sql(query, (act_id,))
            if not table_1:
                return {"status": False, "error": "Activity not found"}, 404
            # Check if the user is allowed to see this activity
            if act_id not in unf.user_flatten(table_1[0]["uids"]):
                return {"status": False, "error": "Unauthorized"}, 403
            return {"status": True, "detail": table_1}, 200

    def create_act(self) -> tuple[int, bool]:
        """
        Create an activity
        Put user in the uids, admin_uids
        Effect:
            set: act_type, uids, admin_uids, due_date, act_title, act_brief
            init: uids, admin_uids, act_aux_info, task_tree
        """
        # Validate required fields

        # Prepare SQL query and parameters
        query = """
            INSERT INTO activity (act_type, uids, admin_uids, due_date, act_title, act_brief, act_aux_info, tasks_tree)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING act_id
        """
        uids = {"creator": self.args["uid"]}
        admin_uids = [self.args["uid"]]
        # Convert due_date string to datetime object
        due_date = datetime.strptime(self.args["due_date"], "%Y-%m-%d %H:%M:%S")

        

        params = (
            self.args["act_type"],
            json.dumps(uids),
            admin_uids,
            due_date,
            self.args["act_title"],
            self.args["act_brief"],
            json.dumps({}),
            json.dumps({}),
        )

        # Execute the query
        result = self.database.run_sql(query, params)
        if not result:
            return -1, False

        # Return success response
        return result[0]["act_id"], True
