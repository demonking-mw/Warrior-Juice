import requests

BASE = "http://127.0.0.1:5000"

response = requests.get(
    BASE + "/activity",
    json={
        "get_all": False,
        "user_name": "smith",
        "act_id": 3,
    },
    timeout=10,
)
print(response.json())
