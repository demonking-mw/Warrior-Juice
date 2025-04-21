"""
put non-crit info into activity test
"""

import sys
import requests
from backend.api_tests import sample_auth

BASE = "http://127.0.0.1:5000"

reauth_token = sample_auth.auth()
act_json = {
    "act_id": 2,
    "is_crit": False,
    "uid": "bob",
    "reauth_jwt": reauth_token,
    "due_date": "2070-02-02 14:30:00",
    "act_title": "chilling",
    "act_brief": "can you kick kittens, no, kitten can't be kicked",
    "tasks_tree": {"task1": 1},
}
response = requests.put(
    BASE + "/activity",
    json=act_json,
    timeout=35,
)
if not response.json().get("status"):
    print("act_put_non_crit failed")
    print(response.json())
    sys.exit(3)
if response.json().get("status"):
    sys.exit(0)
else:
    print("act_put_non_crit failed")
    print(response.json())
    sys.exit(3)
