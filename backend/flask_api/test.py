import requests

BASE = "http://127.0.0.1:5000"

response = requests.post(
    BASE + "/user",
    json={"user_name": "bob", "pwd": "password", "email": "my_email@gmail.com"},
    timeout=10,
)
print(response.json())
