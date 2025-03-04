"""
parse google auth jwt to standard user auth 
"""

import jwt
import os
from dotenv import load_dotenv


class GoogleAuthExtract:
    """
    Authenticate the jwt (not done in the frontend)
    Extract info, and return in a standard format
    """

    def __init__(self, jwt):
        """
        stores the jwt token, potentially other things too
        """
        self.jwt = jwt
        self.decoded = None

    def authenticate(self) -> bool:
        """
        use the auth secret to authenticate the jwt, return bool
        ASSUMPTION: google uses HS256; potential bug
        """
        load_dotenv()
        authsecret = os.getenv("AUTH_SECRET")
        try:
            self.decoded = jwt.decode(self.jwt, authsecret, algorithms=["HS256"])
            return True
        except jwt.ExpiredSignatureError:
            print("Token has expired")
            return False
        except jwt.InvalidTokenError:
            print("Invalid token")
            return False

    def login(self) -> tuple[bool, dict]:
        """
        log in the user by returning required info
        To log in: uid, pwd
        return dict: {"uid": "naeem"}
        """
        if self.decoded is None:
            return False, {}
        return True, {"uid": self.decoded.get("sub")}
        # sub is the unique identifier for the user

    def signup(self) -> tuple[bool, dict]:
        """
        sign up the user by returning required info
        To sign up: uid, pwd, email, user_name
        return dict: {"uid": "naeem
        """
        if self.decoded is None:
            return False, {}
        return True, {
            "email": self.decoded.get("email"),
            "uid": self.decoded.get("sub"),
            "user_name": self.decoded.get("name"),
        }
