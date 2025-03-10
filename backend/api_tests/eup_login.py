'''
tests login with email user password
'''
import sys
import requests

BASE = "http://127.0.0.1:5000"

response = requests.post(
    BASE + "/user",
    json={"type": "eup", "action": "login", "uid": "bob", "pwd": "password"},
    timeout=35,
)
if response.json().get("status"):
    print("complete\n")
    sys.exit(0)
else:
    print("get failed")
    print(response.json())
    sys.exit(3)
