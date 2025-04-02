from files.load_csv import read_csv
from operations.calculate_entropy import calculate_entropies, info_decision
from operations.calculate_gain import calculate_gain
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
    path_tab2 = "../data/testowaTabDec.txt"
    test_entropy(path_gielda)
    test_entropy(path_tab2)
    test_info(path_gielda)
