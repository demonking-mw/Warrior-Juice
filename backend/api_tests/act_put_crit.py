"""
Tests editing crit info of an act
"""

import sys
import requests
from backend.api_tests import sample_auth

# pylint: disable=import-error

BASE = "http://127.0.0.1:5000"
sample_jwt_token = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjI1ZjgyMTE3MTM3ODhiNjE0NTQ3NGI1MDI5YjAxNDFiZDViM2RlOWMiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJhenAiOiI5MzQ3MjgwNTg3MjctanZtM2tldWJqYWx1aWtlZzA2aGw0dm9pZmlxOGZjdjAuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJhdWQiOiI5MzQ3MjgwNTg3MjctanZtM2tldWJqYWx1aWtlZzA2aGw0dm9pZmlxOGZjdjAuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJzdWIiOiIxMTY5MDg3MTE1NjQyNTAxMjQ3MjUiLCJlbWFpbCI6ImJoMzQ5OTM2OTU1QGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJuYmYiOjE3NDExMTYzMTksIm5hbWUiOiJNYXJ2ZW4gV2FuZyIsInBpY3R1cmUiOiJodHRwczovL2xoMy5nb29nbGV1c2VyY29udGVudC5jb20vYS9BQ2c4b2NKbFlyeldzRnJ1N0R4czcwdEd2eS1pcmpTekx6Z18xcVRxd0xWQmUyRlN4cXZPQ0E9czk2LWMiLCJnaXZlbl9uYW1lIjoiTWFydmVuIiwiZmFtaWx5X25hbWUiOiJXYW5nIiwiaWF0IjoxNzQxMTE2NjE5LCJleHAiOjE3NDExMjAyMTksImp0aSI6IjJlNGE4OGIwOWZlMmRlMDQ0MmQxNmVmN2E1ODI0N2YwYjBmNDVkY2QifQ.XNtgvkv_HZ_sBS9_eqL4sqDrur_Xzg30mHRKU8T_yF7wE2mmW9vKZDfCj8locelLZRqQrgODgs5dMDKXP6q6yecQ8bxSRcczFtTkBWUhxjVTiDa_tLmyc9yJdScKhelarIOCGNULBIqL2WW4wT132Zi2zfX5yZi8rs98_b_F4-xu-Hvq-3corI9x6PWvP6Lm4wsvZ_XN2fhTzo3rTyYmclVMZ6PPkkpkUH05k3_np7_OsTKjltINiOyigWUJ7BPkqw1UQ0SVjaew2oRTpj-RrckClwql2mW2oZTmXHwx9V0v34TVh3mazEcpCmkJflpkpOKhWvp8BXr3hlwB4jbCbw"
BASE = "http://127.0.0.1:5000"

response = requests.post(
    BASE + "/user",
    json={"type": "go", "jwt_token": sample_jwt_token},
    timeout=35,
)
if not response.json().get("status"):
    print("oauth get failed")
    print(response.json())
    sys.exit(3)
# get reauth token
oauth_reauth_token = response.json().get("jwt")
# failure
act_json = {
    "act_id": 2,
    "is_crit": True,
    "uid": "116908711564250124725",
    "reauth_jwt": oauth_reauth_token,
    "act_type": "marmoset",
    "user_action": "add",
    "target_uid": "69420",
}
response = requests.put(
    BASE + "/activity",
    json=act_json,
    timeout=35,
)
print(response.json())
if response.json().get("status"):
    print("act_put_crit add succeed with wrong uid")
    print(response.json())
    sys.exit(3)
print("act_put_crit add failed as expected")

reauth_token = sample_auth.auth()
act_json = {
    "act_id": 2,
    "is_crit": True,
    "uid": "bob",
    "reauth_jwt": reauth_token,
    "act_type": "marmoset",
    "user_action": "add",
    "target_uid": "116908711564250124725",
}
response = requests.put(
    BASE + "/activity",
    json=act_json,
    timeout=35,
)
print(response.json())
if not response.json().get("status"):
    print("act_put_crit add failed")
    print(response.json())
    sys.exit(3)

act_json = {
    "act_id": 2,
    "is_crit": True,
    "uid": "bob",
    "reauth_jwt": reauth_token,
    "act_type": "test",
    "user_action": "purge",
    "target_uid": "116908711564250124725",
}
response = requests.put(
    BASE + "/activity",
    json=act_json,
    timeout=35,
)

if response.json().get("status"):
    sys.exit(0)
else:
    print("act_put_crit failed")
    print(response.json())
    sys.exit(3)
