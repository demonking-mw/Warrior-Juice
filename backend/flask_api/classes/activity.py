"""
Operations around activities
"""

# pylint: disable=import-error
import json
from flask_restful import Resource

from backend.flask_api import dbconn, input_req_act as input_req
from backend.logic_classes.helpers import user_name_flatten as unf
from backend.logic_classes.helpers import build_qparser
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
