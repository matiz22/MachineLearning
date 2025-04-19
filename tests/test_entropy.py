from files.load_csv import read_csv
from operations.calculate_entropy import calculate_entropies, info_decision
from operations.calculate_gain import calculate_gain
from operations.calculate_gain_ratio import calculate_gain_ratio
from operations.count_occurrences_columns import count_occurrences


def test_entropy(path):
    dataset = read_csv(path)
    occurs = count_occurrences(dataset)
    print(occurs)
    entropies = calculate_entropies(occurs)
    for i, ent in enumerate(entropies, start=1):
        print(f"Entropia kolumny {i}: {ent}")


def test_info(path):
    dataset = read_csv(path)
    entropies = []
    for i in range(0, len(dataset[0]) - 1):
        e = info_decision(dataset, i)
        entropies.append(e)
        print(e)

    print(calculate_gain(1.0, entropies))


if __name__ == "__main__":
    path_gielda = "../data/gielda.txt"

    dataset = read_csv(path_gielda)
    occurs = count_occurrences(dataset)
    entropies = calculate_entropies(occurs)
    print(f"Entropies for each column {entropies}")

    info_decisions = []
    for i in range(0, len(dataset[0]) - 1):
        e = info_decision(dataset, i)
        info_decisions.append(e)

    print(f"Info for each column {info_decisions}")

    gains = calculate_gain(1.0, info_decisions)
    print(f"Gain for each column {gains}")

    gain_ratios = []
    for idx, val in enumerate(gains):
        gain_ratios.append(calculate_gain_ratio(entropies[idx], val))

    print(f"Gain ratio for each column {gain_ratios}")
