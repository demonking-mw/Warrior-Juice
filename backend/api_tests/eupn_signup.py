"""
tests login with email user password
"""

import sys
import requests

BASE = "http://127.0.0.1:5000"

response = requests.post(
    BASE + "/user",
    json={
        "type": "eup",
        "action": "signup",
        "uid": "peak_workaholism",
        "email": "juice@workaloli.ca",
        "pwd": "password",
        "user_name": "juice",
    },
    timeout=35,
)
if response.json().get("status"):
    print("post complete\n")
    response2 = requests.post(
        BASE + "/user",
        json={
            "type": "eup",
            "action": "delete",
            "uid": "peak_workaholism",
            "email": "juice@workaloli.ca",
            "pwd": "password",
            "user_name": "juice",
        },
        timeout=35,
    )
    if response.json().get("status"):
        print("delete complete\n")
        sys.exit(0)
    else:
        print("delete failed")
        print(response.json())
        sys.exit(3)

else:
    print("post failed")
    print(response.json())
    sys.exit(3)
