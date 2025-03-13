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
            return {"status": False, "detail": self.auth_message}
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
        return {"status": True, "detail": "activities updated successfully"}, 200
