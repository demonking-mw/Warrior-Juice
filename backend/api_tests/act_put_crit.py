"""
Tests editing crit info of an act
"""

import sys
import requests
from backend.api_tests import sample_auth

# pylint: disable=import-error

BASE = "http://127.0.0.1:5000"

reauth_token = sample_auth.auth()
act_json = {
    "act_id": 2,
    "is_crit": True,
    "uid": "bob",
    "reauth_jwt": reauth_token,
    "act_type": "marmoset",
    "user_action": "add",
    "target_uid": "116908711564250124725",
}
response = requests.put(
    BASE + "/activity",
    json=act_json,
    timeout=35,
)
print(response.json())
if not response.json().get("status"):
    print("act_put_crit add failed")
    print(response.json())
    sys.exit(3)

act_json = {
    "act_id": 2,
    "is_crit": True,
    "uid": "bob",
    "reauth_jwt": reauth_token,
    "act_type": "test",
    "user_action": "purge",
    "target_uid": "116908711564250124725",
}
response = requests.put(
    BASE + "/activity",
    json=act_json,
    timeout=35,
)

if response.json().get("status"):
    sys.exit(0)
else:
    print("act_put_crit failed")
    print(response.json())
    sys.exit(3)
