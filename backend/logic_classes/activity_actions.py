'''
Handles the DB side of activities
Takes in a db object
'''

from backend.logic_classes import user_auth
from backend.flask_api import dbconn

class ActivityActions:
    '''
    Default action: auth
    '''
    def __init__(self, database: dbconn.DBConn, args: dict = None) -> None:
        '''
        takes in perspective info in the form of a json with varying fields depending on actions.
        Not having a field for an action will result in failure.
        '''
        self.database = database
        self.args = args
        self.authed = False
        self.new_jwt = None
        auth_class = user_auth.UserAuth(self.database, self.args)
        self.auth_result, self.auth_code = auth_class.login_jwt()
        if self.auth_code == -1:
            print("ERROR:" + str(self.auth_result))

    def get(self) -> tuple[dict, int]:
        '''
        Get the activities for the user
        '''
        if not self.auth_result["status"]:
            return self.auth_result, self.auth_code
        # Get the activities
        
