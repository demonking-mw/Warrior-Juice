"""
helper for flattening nested JSON and extracting user_names
"""


def user_flatten(data: dict) -> list:
    """
    flattens nested JSON and extracts user_names
    """
    user_names = []

    if isinstance(data, dict):  # If data is a dictionary
        for key, value in data.items():
            if isinstance(value, dict):  # If value is a nested JSON (dict)
                user_names.extend(user_flatten(value))
            else:  # Base case: value is a user_name
                user_names.append(value)

    return user_names
