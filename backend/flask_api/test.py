import requests

BASE = "http://127.0.0.1:5000"

response = requests.put(
    BASE + "/user",
    json={"action": "mod_tier", "user_name": "bob", "tier": "pro"},
    timeout=10,
)
print(response.json())
