'''
Parsing class for editing admin user information.
'''

from backend.flask_api import dbconn
from backened.logic_classes import user_auth

class AdminUserEdit:
    '''
    Supports: change password, reset password, email auth, delete user, change username
    '''
    def __init__(self, args: dict):
        '''
        Args from reqparse
        
        '''
        self.args = args
        self.authed = False
        self.auth_type = None
        self.database = dbconn.DBConn()

    def authenticate(self) -> dict:
        '''
        Authenticate user
        Use user_auth class
        Result is reflected in changing self.authed or self.auth_type
        Return dict: status, detail
        '''
        if self.args['auth_type'] == 'email':
            # email auth: recovery password/change info
            # only accept eup
            sql_query = f"SELECT * FROM user_accounts WHERE uid = '{self.args['uid']}';"
            table_1 = self.database.run_sql(sql_query)
            self.database.close()
            if not table_1:
                return {"status": False, "detail": "user not found"}
            if table_1[0]["auth_type"] != "go":
                return {"status": False, "detail": "type is not eup"}
            if "auth_str" not in table_1[0]["aux_info"]:
                return {"status": False, "detail": "auth_str not found in user"}
            authed_answer = table_1[0]["aux_info"]["auth_str"]
            if authed_answer != self.args["auth_str"]:
                return {"status": False, "detail": "auth_str is incorrect"}
            self.authed = True
            self.auth_type = "email"
            return {"status": True, "detail": "authed"}
        # If not email recovery, then user_auth can be used
        auth_class = user_auth.UserAuth(self.args)
        if self.args["auth_type"] == "eup":
            result, code = auth_class.login_up()
        elif self.args["auth_type"] == "go":
            result, code = auth_class.login_go()
        else:
            return {"status": False, "detail": "auth_type not found"}
        if code == -1:
            print("ERROR:" + str(result))
            return {"status": False, "detail": "info mismatch, bug in code"}
        if result["status"]:
            self.authed = True
            self.auth_type = self.args["auth_type"]
            return {"status": True, "detail": "authed"}
        print("user_auth completed but failed")
        return {"status": False, "detail": "auth failed"}

    def edit(self) -> dict:
        '''
        Edit user information
        Return: status, detail
        '''
        if not self.authed:
            return {"status": False, "detail": "not authed"}
        if self.args["action"] == "change":
            # change info that was provided
            # including: password, username
            updates = []
            if "new_pwd" in self.args:
                updates.append(f"pwd = '{self.args['new_pwd']}'")
            if "new_user_name" in self.args:
                updates.append(f"user_name = '{self.args['new_user_name']}'")
            if updates:
                sql_query = f"UPDATE user_accounts SET {', '.join(updates)} WHERE uid = '{self.args['uid']}';"
                self.database.run_sql(sql_query)
                self.database.close()
                return {"status": True, "detail": "user information updated"}
            else:
                return {"status": False, "detail": "no valid fields to update"}
        elif self.args["action"] == "delete":
            # delete account
            sql_query = f"DELETE FROM user_accounts WHERE uid = '{self.args['uid']}';"
            self.database.run_sql(sql_query)
            self.database.close()
            return {"status": True, "detail": "user account deleted"}
        else:
            return {"status": False, "detail": "action not found"}


    def close(self):
        '''
        Close the database connection
        '''
        self.database.close()
