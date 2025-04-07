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
            elif isinstance(value, list):  # If value is a list
                for item in value:
                    user_names.append(item)
            else:  # Base case: value is a user_name
                user_names.append(value)
    else:
        print("ERROR: data is not a dictionary")
    return user_names
