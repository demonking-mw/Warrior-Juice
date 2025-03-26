"""
tests login with email user password
then tests reauth with jwt token
"""

import sys
import requests

BASE = "http://127.0.0.1:5000"


def auth() -> str:
    """
    get a jwt for testing
    """
    response = requests.post(
        BASE + "/user",
        json={"type": "eup", "action": "login", "uid": "bob", "pwd": "password"},
        timeout=35,
    )
    if not response.json().get("status"):
        print("get failed")
        print(response.json())
        sys.exit(3)

    return response.json().get("jwt")
