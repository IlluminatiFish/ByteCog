import math


class JaroDistanceException(Exception):
    def __init__(self, message):
        """
            Enables the usage of the JaroDistanceException class as an exception, 
            which then allows us to 'raise' it as a valid Exception with the :param message:
            
            :param message: Error message being displayed via the class exception
          
            :return: N/A
        """
        super(Exception, self).__init__(message)


def jaro_distance(word_a, word_b, winkler=True, winkler_ajustment=True, scaling=0.1):
    """
        Calculates the Jaro Distance of two strings,
        includes Winkler adjustments to the Jaro Distance Algorithm.

        :param word_a: word to calculate distance for
        :param word_b: word to calculate distance with
        :param winkler: same as winkler_ajustment
        :param winkler_ajustment: add an adjustment factor to the Jaro of the distance
        :param scaling: scaling factor for the Winkler adjustment

        :return: Jaro distance adjusted (or not)
    """

    if not word_a or not word_b:
        raise JaroDistanceException("Cannot calculate distance from NoneType ({0}, {1})".format(
            word_a.__class__.__name__,
            word_b.__class__.__name__))

    jaro = jaro_score(word_a, word_b)
    mini = min(len(get_prefix(word_a, word_b)), 4)

    if all([winkler, winkler_ajustment]):  # 0.1 as scaling factor
        return round((jaro + (scaling * mini * (1.0 - jaro))) * 100.0) / 100.0

    return jaro


def jaro_score(first, second):
    shorter, longer = first.lower(), second.lower()

    if len(first) > len(second):
        longer, shorter = shorter, longer

    match_1 = get_matching_characters(shorter, longer)
    match_2 = get_matching_characters(longer, shorter)

    if len(match_1) == 0 or len(match_2) == 0:
        return 0.0

    return (float(len(match_1)) / len(shorter) +
            float(len(match_2)) / len(longer) +
            float(len(match_1) - transpositions(match_1, match_2)) / len(match_1)) / 3.0


def get_diff_index(first, second):
    if first == second:
        return -1

    if not first or not second:
        return 0

    max_len = min(len(first), len(second))
    for i in range(0, max_len):
        if not first[i] == second[i]:
            return i

    return max_len


def get_prefix(first, second):
    if not first or not second:
        return ""

    index = get_diff_index(first, second)
    if index == -1:
        return first

    elif index == 0:
        return ""

    else:
        return first[0:index]


def get_matching_characters(first, second):
    common = []
    limit = math.floor(min(len(first), len(second)) / 2)

    for i, l in enumerate(first):
        left, right = int(max(0, i - limit)), int(min(i + limit + 1, len(second)))
        if l in second[left:right]:
            common.append(l)
            second = second[0:second.index(l)] + '*' + second[second.index(l) + 1:]

    return ''.join(common)


def transpositions(first, second):
    return math.floor(len([(f, s) for f, s in zip(first, second) if not f == s]) / 2.0)


def string_to_boolean(value):
    true_values = ['true']
    false_values = ['false']

    if value in true_values:
        return True
    elif value in false_values:
        return False
