"""
tests login with email user password
"""

import sys
from backend.api_tests import request_general as RG

req_json = {"type": "eup", "action": "login", "uid": "bob", "pwd": "password"}
exit_code, response = RG.post("/user", req_json)

sys.exit(exit_code)
