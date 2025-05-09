"""
Tests get for act
"""

import sys
import requests
from backend.api_tests import sample_auth

# pylint: disable=import-error

BASE = "http://127.0.0.1:5000"

reauth_token = sample_auth.auth()
act_json = {"uid": "bob", "reauth_jwt": reauth_token, "get_type": "one", "act_id": 2}
response = requests.get(
    BASE + "/activity",
    json=act_json,
    timeout=35,
)
print(response.json())
if response.json().get("status"):
    print("act_get complete\n")
    sys.exit(0)
else:
    print("act_get failed")
    print(response.json())
    sys.exit(3)
