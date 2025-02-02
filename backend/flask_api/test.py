import requests

BASE = "http://127.0.0.1:5000"

response = requests.put(
    BASE + "/user",
    json={"action": "change", "user_name": "bob", "pwd": "bobsmith", "new_pwd": "smth2"},
    timeout=10,
)
print(response.json())
