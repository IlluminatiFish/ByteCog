# Fastest method to get the key of the dictionary that has the highest value
# Reference: https://stackoverflow.com/questions/268272/getting-key-with-maximum-value-in-dictionary
def get_max_key(dictionary):
    values = list(dictionary.values())
    keys = list(dictionary.keys())
    return keys[values.index(max(values))]


def get_value_sorted(dictionary):
    return dict(sorted(dictionary.items(), key=lambda item: item[1], reverse=True))


def list_tuple_merger(list_a, list_b):
    return [(list_a[iterator], list_b[iterator]) for iterator in range(0, len(list_a))]

