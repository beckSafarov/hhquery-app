def find_key_by_value(data, target_value):
    for key, value in data.items():
        if value == target_value:
            return key
    return None


def find_index_by_prop(data, prop, prop_value):
    for index, item in enumerate(data):
        if item.get(prop) == prop_value:
            return index
    return -1  # r


def truncate(text, max_length: int = 25):
    return text if len(text) <= max_length else text[: max_length - 3] + "..."
