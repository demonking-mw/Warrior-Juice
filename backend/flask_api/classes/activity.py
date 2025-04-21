"""
Operations around activities
"""

# pylint: disable=import-error
import json
from flask_restful import Resource

from backend.flask_api import dbconn, input_req_act as input_req
from backend.logic_classes import userinfo_edit
from backend.logic_classes import activity_actions as aa
from backend.logic_classes import actinfo_edit as ae
from backend.logic_classes.helpers import user_name_flatten as unf
from backend.logic_classes.helpers import build_qparser


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
        Calls activity_actions.update_crit() for crit activities
        Calls actinfo_edit for non-crit activities
        
        Args:
        uid/reauth_jwt: str: required
        act_id: int: required
        is_crit: bool: required
        act_type: str: for changing act_type, CRIT, NR
        user_action: str: what to do to uids? put/add/purge, blank for no change, CRIT, NR
        target_uid: str: the uid to work on, CRIT, NR
        uid_tree: dict: updated uid_tree for replacement, CRIT, NR
        uid_path: str: path to insert uid, CRIT, NR, Not Implemented Yet
        admin_action: str: what to do to admin uids? put/add/purge, blank for no change, CRIT, NR
        (uses target_uid)
        due_date: str: new due date, NCRIT, NR
        act_title: str: new activity title, NCRIT, NR
        act_brief: str: new activity brief, NCRIT, NR
        aux_info: dict: new activity aux_info, NCRIT, NR
        tasks_tree: dict: new task tree, NCRIT, NR
        purge_tree: bool: whether to purge tree, NCRIT, NR, default True
        - Side effect: create every task new to the tree, delete every task not in the tree if purge_tree
        - False is for migration of tasks to different activity, should be rare action
        """
        args = input_req.activity_mod.parse_args()
        database = dbconn.DBConn()
        if args["is_crit"]:
            activity_act = aa.ActivityActions(database, args)
            result, code = activity_act.update_crit()
            database.close()
            return result, code
        else:
            actinfo_editor = ae.ActInfoEdit(database, args)
            result, code = actinfo_editor.edit()
            database.close()
            if code == -1:
                return {
                    "status": False,
                    "detail": "internal error, should not happen",
                }, 400
            return result, code
        # Non-crit update not built yet
