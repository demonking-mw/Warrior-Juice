import sys
import requests

BASE = "http://127.0.0.1:5000"

response = requests.post(
    BASE + "/user",
    json={
        "uid": "juice",
        "user_name": "jocelyn",
        "pwd": "",
        "email": "juice@workaholic.lol",
    },
    timeout=35,
)
if response.json().get("status"):
    print("created\n")
    del_response = requests.put(
        BASE + "/user",
        json={
            "action": "delete",
            "user_name": "jocelyn",
            "pwd": "100",
        },
        timeout=35,
    )
    if del_response.json().get("status"):
        print("deleted")
        sys.exit(0)
    else:
        print("delete failed")
        print(del_response.json())
        sys.exit(3)
else:
    print("create failed")
    print(response.json())
    sys.exit(3)
