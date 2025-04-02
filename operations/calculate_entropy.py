import math

from operations.count_occurrences_columns import count_occurrences


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


def info_decision(dataset, column: int):
    occurs = count_occurrences(dataset)[column]
    max_occurs = sum(occurs.values())
    values = []
    for key, value in occurs.items():
        filtered_set = [i for i in dataset if key == i[column]]
        filtered_occurs = count_occurrences(filtered_set)[-1]
        occurs_in_set = sum(filtered_occurs.values())
        proportion = occurs_in_set / max_occurs
        decision = entropy_from_counts(filtered_occurs)
        values.append(proportion * decision)
    return sum(values)
