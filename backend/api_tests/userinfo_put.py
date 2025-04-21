"""
Tests get for act
"""

import sys
import requests
from backend.api_tests import sample_auth
from backend.api_tests import request_general as RG

# pylint: disable=import-error

BASE = "http://127.0.0.1:5000"

reauth_token = sample_auth.auth()
req_json = {
    "reauth_jwt": reauth_token,
    "uid": "bob",
    "target": "sess_list",
    "add_list": "2,3",
    "remove_list": "1",
}
exit_code, response = RG.put("/user/info", req_json, debug_mode=True)
sys.exit(exit_code)
