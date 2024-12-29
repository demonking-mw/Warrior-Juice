import requests

BASE = "http://127.0.0.1:5000"

response = requests.get(BASE + "/user", json={"user_name": "mw_0123", "pwd": 4321})
print(response.json())
