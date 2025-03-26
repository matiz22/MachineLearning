from files.load_csv import read_csv
from operations.count_occurrences_columns import count_occurrences


def test_occurrences(path):
    dataset = read_csv(path)
    print(count_occurrences(dataset))


if __name__ == "__main__":
    path = "../data/test.txt"
    test_occurrences(path)
