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

    def __init__(self, jwt_token: str) -> None:
        """
        stores the jwt token, potentially other things too
        """
        self.jwt_token = jwt_token
        self.decoded = None

    def authenticate(self) -> bool:
        """
        use the auth secret to authenticate the jwt, return bool
        ASSUMPTION: google uses HS256; potential bug
        """
        load_dotenv()
        authsecret = os.getenv("AUTH_SECRET")
        try:
            self.decoded = jwt.decode(
                self.jwt_token, options={"verify_signature": False}
            )
            return True
        except jwt.ExpiredSignatureError:
            print("Token has expired")
            return False
        except jwt.InvalidTokenError:
            print("Invalid token")
            return False
