from collections import Counter


def count_occurrences(dataset: list[list[str]]) -> [dict[str, int]]:
    return [dict(Counter(col)) for col in zip(*dataset)]
