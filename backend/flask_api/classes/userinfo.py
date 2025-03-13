"""
Operations around users
"""

# pylint: disable=import-error
from flask_restful import Resource
from backend.flask_api import input_req
from backend.logic_classes import user_auth, userinfo_edit
from backend.flask_api import dbconn


class UserInfo(Resource):
    """
    Handles the modification of user info
    Such as: user_act_list, user_sess_id, etc
    """

    def get(self):
        """
        Get user info

        Success: return user info and new jwt token
        Fail: relay error from user_auth
        """
        args = input_req.userinfo_get.parse_args()
        database = dbconn.DBConn()
        user_info = user_auth.UserAuth(database, args)
        user_info_json, response_code = user_info.login_jwt()
        if response_code == -1:
            database.close()
            print("ERROR: response code -1" + str(user_info_json))
            return {"status": False, "detail": {"status": "buggy response"}}, 400
        if not user_info_json["status"]:
            database.close()
            return user_info_json, response_code

        database.close()
        return user_info_json, response_code

    def post(self):
        """
        Append new activities/tasks to user
        Use the UserInfoEdit class
        """
        args = input_req.userinfo_post.parse_args()
        database = dbconn.DBConn()
        user_info_edit = userinfo_edit.UserInfoEdit(database, args)
        result = user_info_edit.post()
        database.close()
        return result
