import sys
import requests

BASE = "http://127.0.0.1:5000"

response = requests.post(
    BASE + "/user",
    json={
        "type": "eup",
        "action": "signup",
        "uid": "juice",
        "user_name": "jocelyn",
        "pwd": "0123",
        "email": "juice@workaholic.lol",
    },
    timeout=35,
)
EXIT_CODE = 0
if response.json().get("status"):
    print("created\n")

else:
    print("create failed")
    print(response.json())
    EXIT_CODE = 3

# Duplicate signup
response = requests.post(
    BASE + "/user",
    json={
        "type": "eup",
        "action": "signup",
        "uid": "juice",
        "user_name": "jocelyn",
        "pwd": "0123",
        "email": "juice@workaholic.lol",
    },
    timeout=35,
)
if response.json().get("status"):
    print("Duplicate create should fail")
    EXIT_CODE = -69

else:
    print("create failed as expected")

del_response = requests.put(
    BASE + "/user",
    json={
        "auth_type": "eup",
        "action": "delete",
        "uid": "juice",
        "user_name": "jocelyn",
        "pwd": "0123",
    },
    timeout=35,
)
if del_response.json().get("status"):
    print("deleted")
else:
    print("delete failed")
    print(del_response.json())
    EXIT_CODE = 3

sys.exit(EXIT_CODE)
