"""
tests user eup login and crit mod
"""

import sys
from backend.api_tests import request_general as RG

req_json = {"type": "eup", "action": "login", "uid": "bob", "pwd": "password"}
exit_code, response = RG.post("/user", req_json)
if exit_code == 0:
    reauth_jwt = response.json().get("jwt")
    req_json = {
        "auth_type": "eup",
        "action": "change",
        "uid": "bob",
        "pwd": "password",
        "new_pwd": "password",
    }
    exit_code, response = RG.put("/user", req_json, debug_mode=True)


sys.exit(exit_code)
