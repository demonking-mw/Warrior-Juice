"""
tests login with email user password
then tests reauth with jwt token
"""

import sys
import requests

BASE = "http://127.0.0.1:5000"

response = requests.post(
    BASE + "/user",
    json={"type": "eup", "action": "login", "uid": "bob", "pwd": "password"},
    timeout=35,
)
if not response.json().get("status"):
    print("get failed")
    print(response.json())
    sys.exit(3)

reauth_token = response.json().get("jwt")
print("DEBUG")
print(str(reauth_token))
response = requests.post(
    BASE + "/user",
    json={"type": "jwt", "reauth_jwt": reauth_token, "uid": "bob"},
    timeout=35,
)
if response.json().get("status"):
    print("complete\n")
    sys.exit(0)
else:
    print("reauth failed")
    print(response.json())
    sys.exit(3)  
