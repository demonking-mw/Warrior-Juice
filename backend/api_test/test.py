import requests

BASE = "http://127.0.0.1:5000"

response = requests.get(
    BASE + "/user",
    json={"user_name": "my_name", "pwd": "password"},
    timeout=10,
)
print(response.json())
