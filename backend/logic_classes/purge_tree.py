def purge_tree(data, target_val):
    """
    Recursively remove occurrences of target_val from a dictionary or list.
    If a key in a dictionary has target_val as its value, the key is deleted.
    If an element in a list is target_val, it is removed from the list.
    """
    if isinstance(data, dict):
        # Recursively clean dictionary values
        keys_to_delete = []
        for key, value in data.items():
            cleaned_value = purge_tree(value, target_val)
            if cleaned_value is None:
                keys_to_delete.append(key)  # Mark key for deletion
            else:
                data[key] = cleaned_value  # Update with cleaned value

        for key in keys_to_delete:
            del data[key]  # Remove keys with None values

    elif isinstance(data, list):
        # Recursively clean list elements and remove those that become None
        data[:] = [
            purge_tree(item, target_val)
            for item in data
            if purge_tree(item, target_val) is not None
        ]

    elif data == target_val:
        return None  # Remove target values

    return data
