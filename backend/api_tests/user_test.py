import requests

BASE = "http://127.0.0.1:5000"

response = requests.get(
    BASE + "/user",
    json={
        "user_name": "bob",
        "pwd": "password",
    },
    timeout=35,
)
if response.json().get("status"):
    print("complete")
else:
    print("failed")
    print(response.json())
