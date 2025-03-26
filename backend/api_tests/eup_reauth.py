"""
tests login with email user password
then tests reauth with jwt token
"""

import sys
import requests
from backend.api_tests import sample_auth

# pylint: disable=import-error

BASE = "http://127.0.0.1:5000"

reauth_token = sample_auth.auth()

response = requests.post(
    BASE + "/user",
    json={"type": "jwt", "reauth_jwt": reauth_token, "uid": "bob"},
    timeout=35,
)
if response.json().get("status"):
    print("complete\n")
    if response.json().get("jwt") == reauth_token:
        print("JWT token matches reauth_token")
    else:
        print("JWT token does not match reauth_token")
    sys.exit(0)
else:
    print("reauth failed")
    print(response.json())
    sys.exit(3)
