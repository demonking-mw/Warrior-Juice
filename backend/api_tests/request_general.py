"""
tests login with email user password
"""

import requests

TARGET_URL = "http://127.0.0.1:5000"


def post(
    endpoint: str,
    json_data: dict,
    total_time: int = 35,
    debug_mode: bool = False,
) -> tuple[int, requests.models.Response]:
    """
    post request to endpoint
    """
    response = requests.post(
        TARGET_URL + endpoint,
        json=json_data,
        timeout=total_time,
    )
    if debug_mode:
        print("DEBUG: result json")
        print(str(response.json()))
    if response.json().get("status"):
        if debug_mode:
            print("post request: success")
        return 0, response
    else:
        if debug_mode:
            print("post request: failed")
        return 3, response


def get(
    endpoint: str,
    params: dict = None,
    total_time: int = 35,
    debug_mode: bool = False,
) -> tuple[int, requests.models.Response]:
    """
    get request to endpoint
    """
    response = requests.get(
        TARGET_URL + endpoint,
        params=params,
        timeout=total_time,
    )
    if response.json().get("status"):
        if debug_mode:
            print("get request: success")
        return 0, response
    else:
        if debug_mode:
            print("get request: failed")
        return 3, response


def put(
    endpoint: str,
    json_data: dict,
    total_time: int = 35,
    debug_mode: bool = False,
) -> tuple[int, requests.models.Response]:
    """
    put request to endpoint
    """
    response = requests.put(
        TARGET_URL + endpoint,
        json=json_data,
        timeout=total_time,
    )
    if response.json().get("status"):
        if debug_mode:
            print("put request: success")
        return 0, response
    else:
        if debug_mode:
            print("put request: failed")
        return 3, response


def delete(
    endpoint: str,
    json_data: dict = None,
    total_time: int = 35,
    debug_mode: bool = False,
) -> tuple[int, requests.models.Response]:
    """
    delete request to endpoint
    """
    response = requests.delete(
        TARGET_URL + endpoint,
        json=json_data,
        timeout=total_time,
    )
    if response.json().get("status"):
        if debug_mode:
            print("delete request: success")
        return 0, response
    else:
        if debug_mode:
            print("delete request: failed")
        return 3, response
