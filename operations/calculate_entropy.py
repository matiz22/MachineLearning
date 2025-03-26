import math


def entropy_from_counts(counts):

    total = sum(counts.values())
    if total == 0:
        return 0.0
    entropy = 0.0
    for count in counts.values():
        if count > 0:
            p = count / total
            entropy -= p * math.log2(p)
    return entropy


def calculate_entropies(list_of_counts):
    return [entropy_from_counts(counts) for counts in list_of_counts]
