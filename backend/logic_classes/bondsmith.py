"""
Bonds or unbonds the user with the activity.
"""

from typing import Union


def empty_tree(path: list, target_val) -> dict:
    """
    Returns a nested dict, the last item in path
        is treated as a key, where target_val is inserted
    """
    if len(path) == 0:
        return target_val
    else:
        return {path[0]: empty_tree(path[1:], target_val)}


def bond(
    data: Union[dict, list, str],
    target_val: str,
    path: list = None,
    is_insert: bool = False,
) -> Union[dict, list, str, None]:
    """
    Recursively remove occurrences of target_val from a dictionary or list.
    If a key in a dictionary has target_val as its value, the key is deleted.
    If an element in a list is target_val, it is removed from the list.
    """
    if isinstance(data, dict):
        # Recursively clean dictionary values
        result = {}
        path_found = False
        for key, value in data.items():
            if key == path[0] and is_insert:
                path = path[1:]  # Remove the first item in path
                path_found = True
            cleaned_value = bond(value, target_val, path, is_insert)
            result[key] = cleaned_value
        if not path_found and is_insert:
            if len(path) == 0:
                # Can't insert val only into dict
                raise ValueError(
                    "Cannot insert value into dictionary when path is empty."
                )
            else:
                result[path[0]] = empty_tree(path[1:], target_val)
        return result

    elif isinstance(data, list):
        # Recursively clean list elements and remove those that become None
        if is_insert and len(path) != 0:
            raise ValueError("Cannot insert pathed value into list")
        result = []
        for item in data:
            cleaned_item = bond(item, target_val, path, is_insert)
            if cleaned_item is not None:
                result.append(cleaned_item)
        if is_insert:
            result.append(target_val)
        return result

    elif isinstance(data, str):
        # data is a string
        if is_insert:
            if len(path) != 0:
                raise ValueError("Cannot insert pathed value into string")
            else:
                return [data, target_val]
        else:
            if data == target_val:
                return None
            else:
                return data

    else:
        raise ValueError(
            "Data must be a dictionary, list, or string, data:" + str(data)
        )
