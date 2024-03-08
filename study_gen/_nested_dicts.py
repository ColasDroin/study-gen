# Adapted from https://stackoverflow.com/questions/14692690/access-nested-dictionary-items-via-a-list-of-keys


def nested_get(dic, keys):
    """Get the value from a nested dictionary using a list of keys.

    Args:
        dic (dict): The nested dictionary.
        keys (list): The list of keys to traverse the nested dictionary.

    Returns:
        Any: The value corresponding to the keys in the nested dictionary.

    """
    for key in keys:
        dic = dic[key]
    return dic


def nested_set(dic, keys, value):
    """Set a value in a nested dictionary using a list of keys.

    Args:
        dic (dict): The nested dictionary.
        keys (list): The list of keys to traverse the nested dictionary.
        value (Any): The value to set in the nested dictionary.

    Returns:
        None

    """
    for key in keys[:-1]:
        dic = dic.setdefault(key, {})
    dic[keys[-1]] = value


def nested_del(dic, keys):
    """Delete a value from a nested dictionary using a list of keys.

    Args:
        dic (dict): The nested dictionary.
        keys (list): The list of keys to traverse the nested dictionary.

    Returns:
        None

    """
    for key in keys[:-1]:
        dic = dic[key]
    del dic[keys[-1]]
