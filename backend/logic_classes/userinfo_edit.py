"""
Edit user information that are not admin related
Examples: add/mod/del activities, sessions, calculate scores, etc
"""

from backend.logic_classes import user_auth
from backend.flask_api import dbconn


class UserInfoEdit:
    """
    Edit user information
    """

    def __init__(self, database: dbconn.DBConn, args: dict):
        """
        Args from reqparse
        MUST HAVE:
        jwt_token, uid
        """
        self.database = database
        self.args = args
        self.authed = False
        self.new_jwt = None
        self.auth_message, self.auth_code = self.authenticate()

    def authenticate(self) -> dict:
        """
        Authenticate user
        Use user_auth class
        Result is reflected in changing self.authed or self.auth_type
        Return dict: status, detail
        Changes self.authed
        """
        auth_class = user_auth.UserAuth(self.database, self.args)
        auth_result, code = auth_class.login_jwt()
        if code == -1:
            print("ERROR:" + str(auth_result))
            return {"status": False, "detail": "info mismatch, bug in code"}
        if not auth_result["status"]:
            return {"status": False, "detail": auth_result["detail"]}
        self.authed = True
        self.new_jwt = auth_result.get("jwt")
        return auth_result, code

    def post(self) -> tuple[dict, int]:
        """
        Append new activities/session to user
        Required input: act_ids: list; sess_ids: list
        """
        if not self.authed:
            return self.auth_message, self.auth_code
        if not self.args["act_ids"] and not self.args["sess_ids"]:
            return {"status": False, "detail": "no act_ids or sess_ids provided"}, 400
        act_ids_list = [int(x) for x in self.args["act_ids"].split(",") if x]
        sess_ids_list = [int(x) for x in self.args["sess_ids"].split(",") if x]
        update_query = """
        UPDATE user_accounts
        SET user_act_list = array(
                SELECT DISTINCT unnest(array_cat(user_act_list, %s::int[]))
            ),
            user_sess_id = array(
                SELECT DISTINCT unnest(array_cat(user_sess_id, %s::int[]))
            )
        WHERE uid = %s;
        """
        self.database.run_sql(
            update_query,
            (act_ids_list, sess_ids_list, self.args["uid"]),
        )
        return {
            "status": True,
            "detail": "activities updated successfully",
            "jwt": self.new_jwt,
        }, 200

    def put_list(self):
        """
        Modify user information

        Input spec:
        target: act_list or sess_list
        remove_list: list of act_ids or sess_ids to remove
        add_list: list of act_ids or sess_ids to add
        Basically like github commit, only insert delta

        For act_list, sess_id: returns 2 lists: not removed, not added
        Required input: act_ids: list; sess_ids: list
        """
        if not self.authed:
            return self.auth_message, self.auth_code
        is_act_list = True
        target = self.args["target"]
        if target == "act_list":
            target_list = self.auth_message["detail"]["user_act_list"]
        elif target == "sess_list":
            target_list = self.auth_message["detail"]["user_sess_id"]
            is_act_list = False
        else:
            return {
                "status": False,
                "detail": "target neither act_list nor sess_list",
            }, 400
        to_remove = [int(x) for x in self.args["remove_list"].split(",") if x]
        to_add = [int(x) for x in self.args["add_list"].split(",") if x]
        for item in to_remove[:]:
            if item in target_list:
                target_list.remove(item)
                to_remove.remove(item)
        print("DEBUG: target_list")
        print(target_list)
        for item in to_add[:]:
            print("DEBUG: item")
            print(item)
            if item not in target_list:
                target_list.append(item)
                to_add.remove(item)
        if is_act_list:
            update_query = """
            UPDATE user_accounts
            SET user_act_list = %s
            WHERE uid = %s;
            """
            self.database.run_sql(
                update_query,
                (target_list, self.args["uid"]),
            )
            return {
                "status": True,
                "detail": {"removed": to_remove, "added": to_add},
                "jwt": self.new_jwt,
            }, 200
        else:
            update_query = """
            UPDATE user_accounts
            SET user_sess_id = %s
            WHERE uid = %s;
            """
            self.database.run_sql(
                update_query,
                (target_list, self.args["uid"]),
            )
            return {
                "status": True,
                "detail": {"removed": to_remove, "added": to_add},
                "jwt": self.new_jwt,
            }, 200

    def update_score(self):
        """
        Update user score
        Can be calculate new score base on info or manual update
        """
        return {"status": False, "detail": "Not built yet"}, 500

    def update_efficiency(self):
        """
        Update user efficiency
        Can be calculate new efficiency base on info or manual update
        """
        return {"status": False, "detail": "Not built yet"}, 500
