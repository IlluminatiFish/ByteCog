import math

CHUNK_SIZE = 256


def get_file_entropy(file_path):
    with open(file_path, 'rb') as file:
        data = file.read()
        if data:
            file_entropy = _file_entropy(data)
            return file_entropy


def get_offset_data(file_data):
    counter = 0
    data_size = len(file_data)

    if file_data:
        while counter <= data_size:
            counter += CHUNK_SIZE
            return file_data[counter:counter + CHUNK_SIZE]


def get_file_chunk_entropy(file_data):
    entropy_chunk = []
    offset_chunk = []

    counter = 0
    data_size = len(file_data)

    if file_data:
        while counter <= data_size:
            entropy_chunk.append(_file_entropy(file_data[counter:counter + CHUNK_SIZE]))
            offset_chunk.append(counter)
            counter += CHUNK_SIZE

    return (entropy_chunk, offset_chunk)


def _file_entropy(data):
    possible_values = dict(((chr(char), 0) for char in range(0, 256)))

    for byte in data:
        possible_values[chr(byte)] += 1

    data_size = len(data)
    entropy = 0.0

    for count in possible_values:
        if possible_values[count] == 0:
            continue

        probability = float(possible_values[count] / data_size)
        entropy -= probability * math.log(probability, 2)

    return entropy


