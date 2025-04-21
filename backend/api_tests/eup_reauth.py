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
EXIT_CODE = -1
if response.json().get("status"):
    print("complete\n")
    if response.json().get("jwt") == reauth_token:
        print("JWT token matches reauth_token")
    else:
        print("JWT token does not match reauth_token")
    EXIT_CODE = 0
else:
    print("reauth failed")
    print(response.json())
    EXIT_CODE = 3

broken = reauth_token + "c"
response = requests.post(
    BASE + "/user",
    json={"type": "jwt", "reauth_jwt": broken, "uid": "bob"},
    timeout=35,
)
if response.json().get("status"):
    print("reauth should fail with broken token")
    print(response.json())
    EXIT_CODE = -69
else:
    print("login with wrong password failed as expected")
sys.exit(EXIT_CODE)
