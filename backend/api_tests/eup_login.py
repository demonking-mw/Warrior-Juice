"""
tests login with email user password
also tests userinfo post
"""

import sys
from backend.api_tests import request_general as RG

req_json = {"type": "eup", "action": "login", "uid": "bob", "pwd": "password"}
exit_code, response = RG.post("/user", req_json)
if exit_code == 0:
    reauth_jwt = response.json().get("jwt")
    req_json = {"reauth_jwt": reauth_jwt, "uid": "bob", "act_ids": "1,3"}
    exit_code, response = RG.post("/user/info", req_json, debug_mode=True)

## Failed login
req_json = {"type": "eup", "action": "login", "uid": "bob", "pwd": "dinner_please"}
new_code, response = RG.post("/user", req_json)
if new_code == 0:
    print("ERROR: login with wrong password should fail")
    exit_code = -69  # pylint: disable=invalid-name
else:
    print("login with wrong password failed as expected")

sys.exit(exit_code)
