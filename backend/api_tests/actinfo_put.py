"""
tests login with email user password
"""

import sys
from backend.api_tests import request_general as RG

req_json = {"type": "eup", "action": "login", "uid": "bob", "pwd": "password"}
exit_code, response = RG.post("/user", req_json)
if exit_code == 0:
    reauth_jwt = response.json().get("jwt")
    req_json = {"reauth_jwt": reauth_jwt, "uid": "bob", "target": "act_list", "add_list": "3,4,5", "remove_list": "1,7"}
    exit_code, response = RG.put("/user/info", req_json, debug_mode=True)


sys.exit(exit_code)
