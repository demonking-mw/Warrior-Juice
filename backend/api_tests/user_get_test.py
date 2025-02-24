import sys
import requests

BASE = "http://127.0.0.1:5000"

response = requests.post(
    BASE + "/user",
    json={
        "uid": "juice",
        "user_name": "jocelyn",
        "pwd": "",
    },
    timeout=35,
)
if response.json().get("status"):
    print("complete\n")
    sys.exit(0)
else:
    print("get failed")
    print(response.json())
    sys.exit(3)
