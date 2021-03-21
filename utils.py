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

# Fastest method to get the key of the dictionary that has the highest value
# Reference: https://stackoverflow.com/questions/268272/getting-key-with-maximum-value-in-dictionary
def get_max_key(dictionary):
  
    values = list(dictionary.values())
    keys = list(dictionary.keys())
    
    return keys[values.index(max(values))]

  
def get_value_sorted(dictionary)
    return dict(sorted(dictionary.items(), key=lambda item: item[1], reverse=True))


# This is a mess, does not really use any maths to calculate similarity between both entropy graphs
# TO-DO: Make it actually work, and use some maths to calculate similarity
def calculate_similarity(file_a, file_b, highest_entropy_drift, precision):
  
    chunk_a = len(open(file_a, 'rb').read()) / CHUNK_SIZE
    chunk_b = len(open(file_b, 'rb').read()) / CHUNK_SIZE

    smallest = min(chunk_a, chunk_b)
    highest = max(chunk_a, chunk_b)

    # Lowest amount of chunks divided by the highest amount of chunks
    base_similarity = smallest / highest

    similarity = round(base_similarity * 100, precision)

    return similarity
