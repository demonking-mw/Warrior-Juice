'''
Parsing class for editing admin user information.
'''


class AdminUserEdit:
    '''
    Supports: change password, reset password, email auth, delete user, change username
    '''
    def __init__(self, args: dict):
        '''
        Args from reqparse
        
        '''
        self.args = args

    def authenticate(self):
        '''
        Authenticate user
        Use user_auth class 
        '''
        pass