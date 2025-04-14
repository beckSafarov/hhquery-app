def find_key_by_value(data, target_value):
    for key, value in data.items():
        if value == target_value:
            return key
    return None

